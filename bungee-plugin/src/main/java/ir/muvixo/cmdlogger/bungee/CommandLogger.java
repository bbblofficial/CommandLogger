package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.plugin.Plugin;
import net.md_5.bungee.api.scheduler.ScheduledTask;

import java.util.concurrent.TimeUnit;

/**
 * CommandLogger v2.2 - Broadcasts commands from backend Spigot/Paper servers
 * to staff / OP players on the BungeeCord proxy.
 *
 * Created by Muvixo
 */
public class CommandLogger extends Plugin {

    private Config config;
    private Messages messages;
    private OpPlayerManager opManager;
    private PermissionChecker permissionChecker;
    private BackendMessageReceiver receiver;
    private ScheduledTask opSyncTask;

    @Override
    public void onEnable() {
        if (!getDataFolder().exists()) getDataFolder().mkdirs();

        this.config = new Config(this);
        this.config.load();

        this.messages = new Messages(this);
        this.messages.load();

        this.opManager = new OpPlayerManager(this, config);
        getProxy().getPluginManager().registerListener(this, opManager);

        this.permissionChecker = new PermissionChecker(config, opManager, this);

        this.receiver = new BackendMessageReceiver(this, config, messages, opManager, permissionChecker);
        getProxy().getPluginManager().registerListener(this, receiver);
        getProxy().registerChannel(config.getChannel());

        CommandLoggerBungeeCommand cmd = new CommandLoggerBungeeCommand(
                this, config, messages, opManager, permissionChecker);
        getProxy().getPluginManager().registerCommand(this, cmd);

        int interval = config.getOpStatusIntervalMinutes();
        if (interval > 0) {
            opSyncTask = getProxy().getScheduler().schedule(this, new Runnable() {
                @Override public void run() {}
            }, interval, interval, TimeUnit.MINUTES);
        }

        getLogger().info("===========================================");
        getLogger().info("  CommandLogger v" + getDescription().getVersion());
        getLogger().info("  Created by Muvixo");
        getLogger().info("  Channel: " + config.getChannel());
        getLogger().info("===========================================");
    }

    @Override
    public void onDisable() {
        if (opSyncTask != null) opSyncTask.cancel();
        try { getProxy().unregisterChannel(config.getChannel()); } catch (Exception ignored) {}
        getLogger().info("CommandLogger disabled.");
    }

    public void reloadAll() {
        config.load();
        messages.load();
        getLogger().info("[CommandLogger] Config + messages reloaded.");
    }

    public Config getPluginConfig() { return config; }
    public Messages getMessages() { return messages; }
    public OpPlayerManager getOpManager() { return opManager; }
    public PermissionChecker getPermissionChecker() { return permissionChecker; }
}
