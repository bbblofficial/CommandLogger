package ir.muvixo.cmdlogger.bungee;

import com.google.common.io.ByteArrayDataInput;
import com.google.common.io.ByteStreams;
import net.md_5.bungee.api.ChatColor;
import net.md_5.bungee.api.chat.TextComponent;
import net.md_5.bungee.api.connection.ProxiedPlayer;
import net.md_5.bungee.api.connection.Server;
import net.md_5.bungee.api.event.PluginMessageEvent;
import net.md_5.bungee.api.plugin.Listener;
import net.md_5.bungee.event.EventHandler;

import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.UUID;

/**
 * Receives plugin messages from Spigot/Paper backends on BungeeCord.
 *
 * Created by Muvixo
 */
public class BackendMessageReceiver implements Listener {

    private static final DateTimeFormatter TIME_FORMAT = DateTimeFormatter.ofPattern("HH:mm:ss");

    private final CommandLogger plugin;
    private final Config config;
    private final Messages messages;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;

    public BackendMessageReceiver(CommandLogger plugin, Config config, Messages messages,
                                  OpPlayerManager opManager, PermissionChecker permChecker) {
        this.plugin = plugin;
        this.config = config;
        this.messages = messages;
        this.opManager = opManager;
        this.permChecker = permChecker;
    }

    @EventHandler
    public void onPluginMessage(PluginMessageEvent event) {
        if (!event.getTag().equalsIgnoreCase(config.getChannel())) return;
        event.setCancelled(true);
        if (!(event.getSender() instanceof Server)) return;

        Server server = (Server) event.getSender();
        String sourceServer = server.getInfo().getName();

        try {
            ByteArrayDataInput in = ByteStreams.newDataInput(event.getData());
            String type = in.readUTF();

            if ("OP_STATUS".equals(type)) handleOpStatus(in, sourceServer);
            else if ("CMD".equals(type))  handleCommand(in, sourceServer);
            else plugin.getLogger().warning("[CommandLogger] Unknown message type: " + type);
        } catch (Exception e) {
            plugin.getLogger().warning("[CommandLogger] Failed to decode: " + e.getMessage());
        }
    }

    private void handleOpStatus(ByteArrayDataInput in, String sourceServer) {
        UUID uuid = UUID.fromString(in.readUTF());
        String name = in.readUTF();
        String serverName = in.readUTF();
        boolean isOp = Boolean.parseBoolean(in.readUTF());

        if (isOp) opManager.markOp(uuid, name, serverName);
        else      opManager.unmarkOp(uuid, name);

        if (config.isDebug()) {
            plugin.getLogger().info(messages.raw(
                    isOp ? "console-op-marked" : "console-op-unmarked",
                    "player", name, "server", serverName));
        }
    }

    private void handleCommand(ByteArrayDataInput in, String sourceServer) {
        UUID uuid = UUID.fromString(in.readUTF());
        String name = in.readUTF();
        String serverName = in.readUTF();
        boolean isOp = Boolean.parseBoolean(in.readUTF());
        String command = in.readUTF();

        if (isOp) opManager.markOp(uuid, name, serverName);
        else      opManager.unmarkOp(uuid, name);

        broadcast(name, serverName, command);
    }

    private void broadcast(String playerName, String serverName, String command) {
        String time = LocalTime.now().format(TIME_FORMAT);
        String raw = messages.raw("log-format",
                "player", playerName,
                "server", serverName,
                "command", command,
                "time", time);
        TextComponent message = new TextComponent(
                ChatColor.translateAlternateColorCodes('&', raw));

        int total = 0, sent = 0;
        for (ProxiedPlayer online : plugin.getProxy().getPlayers()) {
            total++;
            if (!permChecker.canSee(online)) continue;
            if (!config.isShowToSelf()
                    && online.getName().equalsIgnoreCase(playerName)) continue;
            online.sendMessage(message);
            sent++;
        }

        if (config.isLogToConsole()) {
            plugin.getLogger().info(messages.raw("console-command-log",
                    "player", playerName,
                    "server", serverName,
                    "command", command,
                    "online", total,
                    "sent", sent,
                    "ops", opManager.getOpCount()));
        }
    }
}
