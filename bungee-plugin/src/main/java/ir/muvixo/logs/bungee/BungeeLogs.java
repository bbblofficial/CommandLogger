package ir.muvixo.logs.bungee;

import net.md_5.bungee.api.plugin.Plugin;
import net.md_5.bungee.api.scheduler.ScheduledTask;

import java.io.File;
import java.util.concurrent.TimeUnit;

/**
 * BungeeLogs v2.2 - Broadcasts commands from backend Spigot/Paper servers
 * to staff / OP players on the BungeeCord proxy.
 *
 * Full BungeeCord 1.8+ support.
 *
 * @author muvixo
 */
public class BungeeLogs extends Plugin {

    private Config config;
    private OpPlayerManager opManager;
    private PermissionChecker permissionChecker;
    private BackendMessageReceiver receiver;
    private ScheduledTask opSyncTask;

    @Override
    public void onEnable() {
        // BungeeCord has no saveDefaultConfig(); Config handles its own defaults.
        if (!getDataFolder().exists()) {
            getDataFolder().mkdirs();
        }

        this.config = new Config(this);
        this.config.load();

        this.opManager = new OpPlayerManager(this, config);
        getProxy().getPluginManager().registerListener(this, opManager);

        this.permissionChecker = new PermissionChecker(config, opManager, this);

        this.receiver = new BackendMessageReceiver(this, config, opManager, permissionChecker);
        getProxy().getPluginManager().registerListener(this, receiver);
        getProxy().registerChannel(config.getChannel());

        BungeeLogsCommand cmd = new BungeeLogsCommand(this, config, opManager, permissionChecker);
        getProxy().getPluginManager().registerCommand(this, cmd);

        // Periodic OP status sync (safety net)
        int interval = config.getOpStatusIntervalMinutes();
        if (interval > 0) {
            opSyncTask = getProxy().getScheduler().schedule(this, new Runnable() {
                @Override
                public void run() {
                    // OP status is reported by backend on join/quit/command.
                    // This task exists as a hook for future expansion.
                }
            }, interval, interval, TimeUnit.MINUTES);
        }

        getLogger().info("===========================================");
        getLogger().info("  BungeeLogs v" + getDescription().getVersion());
        getLogger().info("  Channel: " + config.getChannel());
        getLogger().info("  Report OP: " + config.isReportOpStatus());
        getLogger().info("  Debug: " + config.isDebug());
        getLogger().info("===========================================");
    }

    @Override
    public void onDisable() {
        if (opSyncTask != null) {
            opSyncTask.cancel();
        }
        try {
            getProxy().unregisterChannel(config.getChannel());
        } catch (Exception ignored) {}
        getLogger().info("BungeeLogs disabled.");
    }

    public void reloadAll() {
        config.load();
        getLogger().info("[BungeeLogs] Config reloaded.");
    }

    // ============================================================
    //  GETTERS
    // ============================================================
    public Config getPluginConfig() { return config; }
    public OpPlayerManager getOpManager() { return opManager; }
    public PermissionChecker getPermissionChecker() { return permissionChecker; }
}
