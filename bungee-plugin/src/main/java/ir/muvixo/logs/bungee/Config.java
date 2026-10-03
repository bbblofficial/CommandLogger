package ir.muvixo.logs.bungee;

import net.md_5.bungee.config.Configuration;
import net.md_5.bungee.config.ConfigurationProvider;
import net.md_5.bungee.config.YamlConfiguration;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Config wrapper for BungeeLogs v2.2.
 *
 * @author muvixo
 */
public class Config {

    private final BungeeLogs plugin;

    private String channel;
    private String messageFormat;
    private String reloadSuccessMessage;
    private String noPermissionMessage;
    private boolean showToSelf;
    private boolean logToConsole;
    private boolean debug;
    private boolean reportOpStatus;
    private int opCacheExpireMinutes;
    private int opStatusIntervalMinutes;
    private String seePermission;
    private String adminPermission;

    public Config(BungeeLogs plugin) {
        this.plugin = plugin;
    }

    public void load() {
        try {
            if (!plugin.getDataFolder().exists()) {
                plugin.getDataFolder().mkdirs();
            }

            File file = new File(plugin.getDataFolder(), "config.yml");
            if (!file.exists()) {
                try (InputStream in = plugin.getResourceAsStream("config.yml")) {
                    if (in != null) {
                        Files.copy(in, file.toPath());
                    }
                }
            }

            Configuration cfg = ConfigurationProvider.getProvider(YamlConfiguration.class).load(file);

            this.channel = cfg.getString("channel", "velocitylogs:main");
            this.showToSelf = cfg.getBoolean("show-to-self", false);
            this.logToConsole = cfg.getBoolean("log-to-console", true);
            this.debug = cfg.getBoolean("debug", false);
            this.reportOpStatus = cfg.getBoolean("report-op-status", true);
            this.opCacheExpireMinutes = cfg.getInt("op-cache-expire-minutes", 5);
            this.opStatusIntervalMinutes = cfg.getInt("op-status-interval-minutes", 1);

            this.messageFormat = cfg.getString("message-format",
                    "&8[&cLogs&8] &e{player} &8>> &b{server} &8>> &f/{command}");
            this.reloadSuccessMessage = cfg.getString("reload-success-message",
                    "&a[OK] Config reloaded successfully!");
            this.noPermissionMessage = cfg.getString("no-permission-message",
                    "&c[!] You don't have permission to do that!");

            this.seePermission = cfg.getString("permissions.see", "velocitylogs.see");
            this.adminPermission = cfg.getString("permissions.admin", "velocitylogs.admin");

        } catch (IOException e) {
            plugin.getLogger().severe("Could not load config.yml: " + e.getMessage());
        }
    }

    public String getChannel() { return channel; }
    public String getMessageFormat() { return messageFormat; }
    public String getReloadSuccessMessage() { return reloadSuccessMessage; }
    public String getNoPermissionMessage() { return noPermissionMessage; }
    public boolean isShowToSelf() { return showToSelf; }
    public boolean isLogToConsole() { return logToConsole; }
    public boolean isDebug() { return debug; }
    public boolean isReportOpStatus() { return reportOpStatus; }
    public int getOpCacheExpireMinutes() { return opCacheExpireMinutes; }
    public int getOpStatusIntervalMinutes() { return opStatusIntervalMinutes; }
    public String getSeePermission() { return seePermission; }
    public String getAdminPermission() { return adminPermission; }
}
