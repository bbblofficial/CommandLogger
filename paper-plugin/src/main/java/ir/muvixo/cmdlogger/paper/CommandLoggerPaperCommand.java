package ir.muvixo.cmdlogger.paper;

import java.util.ArrayList;
import java.util.List;

import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;

/**
 * /clogs - Paper side command, fully driven by messages.yml.
 *
 * Created by Muvixo
 */
public class CommandLoggerPaperCommand implements CommandExecutor, TabCompleter {

    private static final String LABEL = "clogs";

    private final CommandLogger plugin;
    private final Config config;
    private final Messages messages;

    public CommandLoggerPaperCommand(CommandLogger plugin, Config config, Messages messages) {
        this.plugin = plugin;
        this.config = config;
        this.messages = messages;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command command,
                             String label, String[] args) {
        if (args.length == 0) { sendHelp(sender); return true; }
        String sub = args[0].toLowerCase();

        if (sub.equals("help") || sub.equals("?")) { sendHelp(sender); return true; }

        if (sub.equals("creator") || sub.equals("author")) {
            if (!sender.hasPermission(getPerm("creator", "commandlogger.creator"))) {
                noPerm(sender); return true;
            }
            sendCreator(sender);
            return true;
        }
        if (sub.equals("info")) {
            if (!sender.hasPermission(getPerm("use", "commandlogger.use"))) {
                noPerm(sender); return true;
            }
            sendInfo(sender);
            return true;
        }
        if (sub.equals("status")) {
            if (!sender.hasPermission(getPerm("status", "commandlogger.status"))) {
                noPerm(sender); return true;
            }
            sendStatus(sender);
            return true;
        }
        if (sub.equals("reload")) {
            if (!sender.hasPermission(getPerm("reload", "commandlogger.reload"))) {
                noPerm(sender); return true;
            }
            plugin.reloadAll();
            sender.sendMessage(messages.color("reload-success"));
            return true;
        }
        if (sub.equals("toggle")) {
            if (!sender.hasPermission(getPerm("toggle", "commandlogger.toggle"))) {
                noPerm(sender); return true;
            }
            boolean now = !plugin.isForwardingEnabled();
            plugin.setForwardingEnabled(now);
            sender.sendMessage(messages.color(now ? "forwarding-enabled" : "forwarding-disabled"));
            return true;
        }
        if (sub.equals("debug")) {
            if (!sender.hasPermission(getPerm("debug", "commandlogger.debug"))) {
                noPerm(sender); return true;
            }
            boolean now = !plugin.isDebugEnabled();
            plugin.setDebugEnabled(now);
            sender.sendMessage(messages.color(now ? "debug-enabled" : "debug-disabled"));
            return true;
        }

        sender.sendMessage(messages.color("unknown-subcommand", "label", LABEL));
        return true;
    }

    private String getPerm(String action, String defaultPerm) {
        String value = plugin.getConfig().getString("permissions." + action);
        if (value == null || value.trim().isEmpty()) return defaultPerm;
        return value.trim();
    }

    private void sendHelp(CommandSender sender) {
        String permUse     = getPerm("use",     "commandlogger.use");
        String permCreator = getPerm("creator", "commandlogger.creator");
        String permAdmin   = getPerm("admin",   "commandlogger.admin");
        String permReload  = getPerm("reload",  "commandlogger.reload");
        String permStatus  = getPerm("status",  "commandlogger.status");
        String permToggle  = getPerm("toggle",  "commandlogger.toggle");
        String permDebug   = getPerm("debug",   "commandlogger.debug");

        boolean isAdmin = sender.hasPermission(permAdmin)
                || sender.hasPermission(permReload)
                || sender.hasPermission(permStatus)
                || sender.hasPermission(permToggle)
                || sender.hasPermission(permDebug);
        boolean isUser = sender.hasPermission(permUse) || sender.hasPermission(permCreator);

        if (!isAdmin && !isUser) { noPerm(sender); return; }

        sender.sendMessage(messages.color("help-header"));
        sender.sendMessage(messages.color("help-title"));
        sender.sendMessage(messages.color("help-header"));

        sender.sendMessage(messages.color("help-section-general"));
        sender.sendMessage(messages.color("help-line-help", "label", LABEL));

        if (sender.hasPermission(permCreator))
            sender.sendMessage(messages.color("help-line-creator", "label", LABEL));
        if (sender.hasPermission(permUse))
            sender.sendMessage(messages.color("help-line-info", "label", LABEL));

        if (isAdmin) {
            sender.sendMessage(messages.color("help-header"));
            sender.sendMessage(messages.color("help-section-admin"));
            if (sender.hasPermission(permStatus))
                sender.sendMessage(messages.color("help-line-status", "label", LABEL));
            if (sender.hasPermission(permToggle))
                sender.sendMessage(messages.color("help-line-op", "label", LABEL));
            if (sender.hasPermission(permDebug))
                sender.sendMessage(messages.color("help-line-debug", "label", LABEL));
            if (sender.hasPermission(permReload))
                sender.sendMessage(messages.color("help-line-reload", "label", LABEL));
        }

        sender.sendMessage(messages.color("help-footer"));
    }

    private void sendCreator(CommandSender sender) {
        sender.sendMessage(messages.color("creator-line-1"));
        sender.sendMessage(messages.color("creator-line-2"));
        sender.sendMessage(messages.color("creator-line-3"));
        sender.sendMessage(messages.color("creator-line-4"));
    }

    private void sendInfo(CommandSender sender) {
        sender.sendMessage(messages.color("info-header"));
        sender.sendMessage(messages.color("info-title"));
        sender.sendMessage(messages.color("info-channel", "channel", config.getChannel()));
        sender.sendMessage(messages.color("info-server", "server", config.getServerName()));
        sender.sendMessage(messages.color("info-log-ops", "value", String.valueOf(config.isLogOps())));
        sender.sendMessage(messages.color("info-report-op", "value",
                String.valueOf(config.isReportOpStatus())));
        sender.sendMessage(messages.color("info-footer"));
    }

    private void sendStatus(CommandSender sender) {
        sender.sendMessage(messages.color("info-header"));
        sender.sendMessage(messages.color("info-title"));
        sender.sendMessage(messages.color("info-forwarding", "value",
                messages.raw(plugin.isForwardingEnabled() ? "status-enabled" : "status-disabled")));
        sender.sendMessage(messages.color("info-debug", "value",
                messages.raw(plugin.isDebugEnabled() ? "status-on" : "status-off")));
        sender.sendMessage(messages.color("info-channel", "channel", config.getChannel()));
        sender.sendMessage(messages.color("info-server", "server", config.getServerName()));
        sender.sendMessage(messages.color("info-log-ops", "value", String.valueOf(config.isLogOps())));
        sender.sendMessage(messages.color("info-footer"));
    }

    private void noPerm(CommandSender sender) { sender.sendMessage(messages.color("no-permission")); }

    @Override
    public List<String> onTabComplete(CommandSender sender, Command command,
                                      String alias, String[] args) {
        List<String> out = new ArrayList<String>();
        if (args.length == 1) {
            List<String> subs = new ArrayList<String>();
            boolean isAdmin = sender.hasPermission(getPerm("admin",  "commandlogger.admin"))
                    || sender.hasPermission(getPerm("reload", "commandlogger.reload"))
                    || sender.hasPermission(getPerm("status", "commandlogger.status"))
                    || sender.hasPermission(getPerm("toggle", "commandlogger.toggle"))
                    || sender.hasPermission(getPerm("debug",  "commandlogger.debug"));
            boolean isUser = sender.hasPermission(getPerm("use",     "commandlogger.use"))
                    || sender.hasPermission(getPerm("creator", "commandlogger.creator"));
            if (!isAdmin && !isUser) return out;

            subs.add("help");
            if (sender.hasPermission(getPerm("creator", "commandlogger.creator"))) subs.add("creator");
            if (sender.hasPermission(getPerm("use",     "commandlogger.use")))     subs.add("info");
            if (sender.hasPermission(getPerm("status",  "commandlogger.status")))  subs.add("status");
            if (sender.hasPermission(getPerm("toggle",  "commandlogger.toggle")))  subs.add("toggle");
            if (sender.hasPermission(getPerm("debug",   "commandlogger.debug")))   subs.add("debug");
            if (sender.hasPermission(getPerm("reload",  "commandlogger.reload")))  subs.add("reload");

            String partial = args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
        }
        return out;
    }
}
