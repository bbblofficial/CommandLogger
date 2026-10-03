package ir.muvixo.logs.bungee;

import net.md_5.bungee.api.connection.ProxiedPlayer;
import net.md_5.bungee.api.event.PlayerDisconnectEvent;
import net.md_5.bungee.api.event.ServerConnectedEvent;
import net.md_5.bungee.api.plugin.Listener;
import net.md_5.bungee.event.EventHandler;

import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Tracks which players are OP on a backend server.
 *
 * @author muvixo
 */
public class OpPlayerManager implements Listener {

    public static class OpRecord {
        public final UUID uuid;
        public volatile String name;
        public volatile String serverName;
        public volatile long lastSeen;

        public OpRecord(UUID uuid, String name, String serverName) {
            this.uuid = uuid;
            this.name = name;
            this.serverName = serverName;
            this.lastSeen = System.currentTimeMillis();
        }

        public void refresh(String serverName) {
            this.serverName = serverName;
            this.lastSeen = System.currentTimeMillis();
        }
    }

    private final BungeeLogs plugin;
    private final Config config;
    private final Map<UUID, OpRecord> opPlayers = new ConcurrentHashMap<UUID, OpRecord>();
    private final Map<String, UUID> nameIndex = new ConcurrentHashMap<String, UUID>();

    public OpPlayerManager(BungeeLogs plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    public void markOp(UUID uuid, String playerName, String serverName) {
        if (uuid == null) return;

        OpRecord existing = opPlayers.get(uuid);
        if (existing != null) {
            if (playerName != null && !playerName.equalsIgnoreCase(existing.name)) {
                nameIndex.remove(existing.name.toLowerCase());
                nameIndex.put(playerName.toLowerCase(), uuid);
                existing.name = playerName;
            }
            existing.refresh(serverName);
            return;
        }

        OpRecord rec = new OpRecord(uuid, playerName, serverName);
        opPlayers.put(uuid, rec);
        if (playerName != null) {
            nameIndex.put(playerName.toLowerCase(), uuid);
        }
        if (config.isDebug()) {
            plugin.getLogger().info("[OP-TRACK] Marked " + playerName + " (" + uuid + ") as OP (backend: " + serverName + ")");
        }
    }

    public void unmarkOp(UUID uuid, String playerName) {
        if (uuid == null) return;

        OpRecord removed = opPlayers.remove(uuid);
        if (removed != null) {
            nameIndex.remove(removed.name.toLowerCase());
            if (config.isDebug()) {
                plugin.getLogger().info("[OP-TRACK] Unmarked " + removed.name + " (" + uuid + ")");
            }
        }
        if (playerName != null) {
            nameIndex.remove(playerName.toLowerCase());
        }
    }

    public boolean isOp(UUID uuid) {
        if (uuid == null) return false;
        OpRecord rec = opPlayers.get(uuid);
        if (rec == null) return false;

        int expire = config.getOpCacheExpireMinutes();
        if (expire > 0) {
            ProxiedPlayer player = plugin.getProxy().getPlayer(uuid);
            boolean online = player != null && player.isConnected();
            long age = System.currentTimeMillis() - rec.lastSeen;
            if (!online && age > expire * 60_000L) {
                opPlayers.remove(uuid);
                nameIndex.remove(rec.name.toLowerCase());
                return false;
            }
        }
        return true;
    }

    public boolean isOpByName(String name) {
        if (name == null) return false;
        UUID uuid = nameIndex.get(name.toLowerCase());
        return uuid != null && isOp(uuid);
    }

    public String getOpServer(UUID uuid) {
        OpRecord rec = opPlayers.get(uuid);
        return rec == null ? null : rec.serverName;
    }

    public int getOpCount() {
        return opPlayers.size();
    }

    public Map<UUID, OpRecord> getOpPlayers() {
        return opPlayers;
    }

    @EventHandler
    public void onDisconnect(PlayerDisconnectEvent event) {
        UUID uuid = event.getPlayer().getUniqueId();
        OpRecord rec = opPlayers.get(uuid);
        if (rec != null) {
            rec.lastSeen = System.currentTimeMillis();
        }
    }

    @EventHandler
    public void onServerConnected(ServerConnectedEvent event) {
        if (config.isDebug()) {
            plugin.getLogger().info("[OP-TRACK] " + event.getPlayer().getName()
                    + " connected to " + event.getServer().getInfo().getName()
                    + " (OP status: " + isOp(event.getPlayer().getUniqueId()) + ")");
        }
    }
}
