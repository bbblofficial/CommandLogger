package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.ChatColor;
import net.md_5.bungee.api.CommandSender;
import net.md_5.bungee.api.chat.TextComponent;
import net.md_5.bungee.api.connection.ProxiedPlayer;
import net.md_5.bungee.api.plugin.Command;
import net.md_5.bungee.api.plugin.TabExecutor;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * /clogs command for BungeeCord, fully driven by messages.yml.
 *
 * Created by Muvixo
 */
public class CommandLoggerBungeeCommand extends Command implements TabExecutor {

    private static final String LABEL = "clogs";

    private final CommandLogger plugin;
    private final Config config;
    private final Messages messages;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;

    public CommandLoggerBungeeCommand(CommandLogger plugin, Config config, Messages messages,
                                      OpPlayerManager opManager, PermissionChecker permChecker) {
        super("clogs", null, "clog", "cmdlogger", "cmdlogs");
        this.plugin = plugin;
        this.config = config;
        this.messages = messages;
        this.opManager = opManager;
        this.permChecker = permChecker;
    }

    @Override
    public void execute(CommandSender sender, String[] args) {
        if (args.length == 0) { sendHelp(sender); return; }
        String sub = args[0].toLowerCase();

        if (sub.equals("help") || sub.equals("?")) { sendHelp(sender); return; }

        if (sub.equals("info")) {
            if (!canUse(sender)) { noPerm(sender); return; }
            sendInfo(sender);
            return;
        }
        if (sub.equals("creator") || sub.equals("author")) {
            if (!canUse(sender)) { noPerm(sender); return; }
            sendCreator(sender);
            return;
        }
        if (sub.equals("reload")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            plugin.reloadAll();
            sender.sendMessage(tx("reload-success"));
            return;
        }
        if (sub.equals("list")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            sendOpList(sender);
            return;
        }
        if (sub.equals("op")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) { sender.sendMessage(tx("usage-op", "label", LABEL)); return; }
            ProxiedPlayer t = plugin.getProxy().getPlayer(args[1]);
            if (t == null) { sender.sendMessage(tx("player-not-found", "player", args[1])); return; }
            opManager.markOp(t.getUniqueId(), t.getName(), "manual");
            sender.sendMessage(tx("marked-op", "player", args[1]));
            return;
        }
        if (sub.equals("unop")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) { sender.sendMessage(tx("usage-unop", "label", LABEL)); return; }
            ProxiedPlayer t = plugin.getProxy().getPlayer(args[1]);
            if (t == null) { sender.sendMessage(tx("player-not-found", "player", args[1])); return; }
            opManager.unmarkOp(t.getUniqueId(), t.getName());
            sender.sendMessage(tx("unmarked-op", "player", args[1]));
            return;
        }
        if (sub.equals("debug") || sub.equals("status")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(tx(sub.equals("debug") ? "usage-debug" : "usage-status",
                        "label", LABEL));
                return;
            }
            ProxiedPlayer t = plugin.getProxy().getPlayer(args[1]);
            if (t == null) { sender.sendMessage(tx("player-not-found", "player", args[1])); return; }
            sendDebug(sender, t);
            return;
        }

        sender.sendMessage(tx("unknown-subcommand", "label", LABEL));
    }

    private boolean canUse(CommandSender sender) {
        if (!(sender instanceof ProxiedPlayer)) return true;
        return permChecker.canSee((ProxiedPlayer) sender);
    }

    private boolean canReload(CommandSender sender) {
        if (!(sender instanceof ProxiedPlayer)) return true;
        return permChecker.canReload((ProxiedPlayer) sender);
    }

    private void sendHelp(CommandSender sender) {
        boolean isAdmin = canReload(sender);
        boolean isUser  = canUse(sender);
        if (!isAdmin && !isUser) { noPerm(sender); return; }

        sender.sendMessage(tx("help-header"));
        sender.sendMessage(tx("help-title"));
        sender.sendMessage(tx("help-header"));

        sender.sendMessage(tx("help-section-general"));
        sender.sendMessage(tx("help-line-help", "label", LABEL));

        if (isUser) {
            sender.sendMessage(tx("help-line-info", "label", LABEL));
            sender.sendMessage(tx("help-line-creator", "label", LABEL));
        }
        if (isAdmin) {
            sender.sendMessage(tx("help-header"));
            sender.sendMessage(tx("help-section-admin"));
            sender.sendMessage(tx("help-line-reload", "label", LABEL));
            sender.sendMessage(tx("help-line-list", "label", LABEL));
            sender.sendMessage(tx("help-line-op", "label", LABEL));
            sender.sendMessage(tx("help-line-unop", "label", LABEL));
            sender.sendMessage(tx("help-line-debug", "label", LABEL));
            sender.sendMessage(tx("help-line-status", "label", LABEL));
        }
        sender.sendMessage(tx("help-footer"));
    }

    private void sendInfo(CommandSender sender) {
        sender.sendMessage(tx("info-header"));
        sender.sendMessage(tx("info-title"));
        sender.sendMessage(tx("info-channel", "channel", config.getChannel()));
        sender.sendMessage(tx("info-log-ops", "value", String.valueOf(config.isReportOpStatus())));
        sender.sendMessage(tx("info-debug", "value",
                messages.raw(config.isDebug() ? "status-on" : "status-off")));
        sender.sendMessage(tx("info-tracked-ops", "ops", opManager.getOpCount()));
        sender.sendMessage(tx("info-footer"));
    }

    private void sendCreator(CommandSender sender) {
        sender.sendMessage(tx("creator-line-1"));
        sender.sendMessage(tx("creator-line-2"));
        sender.sendMessage(tx("creator-line-3"));
        sender.sendMessage(tx("creator-line-4"));
    }

    private void sendOpList(CommandSender sender) {
        Map<UUID, OpPlayerManager.OpRecord> ops = opManager.getOpPlayers();
        sender.sendMessage(tx("help-header"));
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "Tracked OPs (" + ops.size() + ")"));
        sender.sendMessage(tx("help-header"));

        if (ops.isEmpty()) {
            sender.sendMessage(new TextComponent(ChatColor.GRAY + "  (none)"));
            sender.sendMessage(tx("help-footer"));
            return;
        }
        long now = System.currentTimeMillis();
        for (OpPlayerManager.OpRecord r : ops.values()) {
            long ageSec = (now - r.lastSeen) / 1000;
            sender.sendMessage(new TextComponent(ChatColor.GRAY
                    + String.format("  %s | server=%s | lastSeen=%ds ago",
                    r.name, r.serverName, ageSec)));
        }
        sender.sendMessage(tx("help-footer"));
    }

    private void sendDebug(CommandSender sender, ProxiedPlayer player) {
        boolean isOp = opManager.isOp(player.getUniqueId());
        String opServer = opManager.getOpServer(player.getUniqueId());
        boolean canSee = permChecker.canSee(player);

        sender.sendMessage(tx("debug-header"));
        sender.sendMessage(tx("debug-title", "player", player.getName()));
        sender.sendMessage(tx("debug-uuid", "uuid", player.getUniqueId()));
        sender.sendMessage(tx("debug-tracked-op", "value",
                messages.raw(isOp ? "debug-yes" : "debug-no")));
        sender.sendMessage(tx("debug-op-server", "server",
                opServer == null ? messages.raw("debug-unknown") : opServer));
        sender.sendMessage(tx("debug-can-see", "value",
                messages.raw(canSee ? "debug-yes" : "debug-no")));
        sender.sendMessage(tx("debug-result", "value",
                messages.raw(canSee ? "debug-yes" : "debug-no")));
        sender.sendMessage(tx("debug-footer"));
    }

    private void noPerm(CommandSender sender) { sender.sendMessage(tx("no-permission")); }

    private TextComponent tx(String key, Object... kv) {
        return new TextComponent(ChatColor.translateAlternateColorCodes('&',
                messages.raw(key, kv)));
    }

    @Override
    public Iterable<String> onTabComplete(CommandSender sender, String[] args) {
        List<String> out = new ArrayList<String>();
        if (args.length <= 1) {
            boolean isAdmin = canReload(sender);
            boolean isUser  = canUse(sender);
            if (!isAdmin && !isUser) return out;

            List<String> subs = new ArrayList<String>();
            subs.add("help");
            if (isUser) { subs.add("info"); subs.add("creator"); }
            if (isAdmin) {
                subs.add("reload"); subs.add("list");
                subs.add("op"); subs.add("unop");
                subs.add("debug"); subs.add("status");
            }
            String partial = args.length == 0 ? "" : args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
            return out;
        }
        if (args.length == 2) {
            String sub = args[0].toLowerCase();
            if ((sub.equals("debug") || sub.equals("status")
                    || sub.equals("op") || sub.equals("unop")) && canReload(sender)) {
                String partial = args[1].toLowerCase();
                for (ProxiedPlayer p : plugin.getProxy().getPlayers()) {
                    if (p.getName().toLowerCase().startsWith(partial)) out.add(p.getName());
                }
            }
        }
        return out;
    }
}
