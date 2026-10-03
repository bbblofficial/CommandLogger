package ir.muvixo.cmdlogger.spigot;

import com.google.common.io.ByteArrayDataOutput;
import com.google.common.io.ByteStreams;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerCommandPreprocessEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

/**
 * Intercepts EVERY command a player types and forwards them to the proxy.
 *
 * Created by Muvixo
 */
public class CommandInterceptor implements Listener {

    private final CommandLogger plugin;
    private final Config config;

    public CommandInterceptor(CommandLogger plugin, Config config) {
        this.plugin = plugin;
        this.config = config;
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onJoin(PlayerJoinEvent event) {
        if (!config.isReportOpStatus()) return;
        final Player player = event.getPlayer();
        plugin.getServer().getScheduler().runTaskLater(plugin, new Runnable() {
            @Override
            public void run() {
                if (player.isOnline()) {
                    plugin.sendOpStatus(player, player.isOp());
                }
            }
        }, 20L);
    }

    @EventHandler(priority = EventPriority.MONITOR)
    public void onQuit(PlayerQuitEvent event) {
        if (!config.isReportOpStatus()) return;
        plugin.sendOpStatus(event.getPlayer(), false);
    }

    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = false)
    public void onCommand(PlayerCommandPreprocessEvent event) {

        if (!plugin.isForwardingEnabled()) return;

        Player player = event.getPlayer();

        if (config.isReportOpStatus()) {
            plugin.sendOpStatus(player, player.isOp());
        }

        if (!config.isLogOps() && player.isOp()) return;
        if (config.isIgnoredPlayer(player.getName())) return;

        String full = event.getMessage();
        if (full == null || full.isEmpty()) return;

        if (full.charAt(0) != '/') return;

        String command = full.substring(1).trim();
        if (command.isEmpty()) return;

        String base = command.split(" ", 2)[0].toLowerCase();
        if (base.equals("clogs") || base.equals("clog") || base.equals("cmdlogger")) return;

        if (config.isBlacklisted(command)) return;

        try {
            ByteArrayDataOutput out = ByteStreams.newDataOutput();
            out.writeUTF("CMD");
            out.writeUTF(player.getUniqueId().toString());
            out.writeUTF(player.getName());
            out.writeUTF(config.getServerName());
            out.writeUTF(Boolean.toString(player.isOp()));
            out.writeUTF(command);
            player.sendPluginMessage(plugin, config.getChannel(), out.toByteArray());

            if (plugin.isDebugEnabled()) {
                plugin.getLogger().info("[DEBUG] Forwarded: " + player.getName()
                        + " (op=" + player.isOp() + ") -> /" + command);
            }
        } catch (Exception e) {
            plugin.getLogger().warning("Failed to forward command: " + e.getMessage());
        }
    }
}
