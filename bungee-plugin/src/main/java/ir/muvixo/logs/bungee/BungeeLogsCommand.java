package ir.muvixo.logs.bungee;

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
 * /logs command for BungeeCord with a permission-aware help menu.
 *
 * @author muvixo
 */
public class BungeeLogsCommand extends Command implements TabExecutor {

    private final BungeeLogs plugin;
    private final Config config;
    private final OpPlayerManager opManager;
    private final PermissionChecker permChecker;

    public BungeeLogsCommand(BungeeLogs plugin, Config config,
                             OpPlayerManager opManager, PermissionChecker permChecker) {
        super("logs", null, "vlogs", "bungeelogs", "cmdlogs", "commandlogs");
        this.plugin = plugin;
        this.config = config;
        this.opManager = opManager;
        this.permChecker = permChecker;
    }

    @Override
    public void execute(CommandSender sender, String[] args) {
        if (args.length == 0) { sendHelp(sender); return; }

        String sub = args[0].toLowerCase();

        if (sub.equals("help") || sub.equals("?")) {
            sendHelp(sender);
            return;
        }

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
            sender.sendMessage(new TextComponent(ChatColor.translateAlternateColorCodes('&',
                    config.getReloadSuccessMessage())));
            return;
        }

        if (sub.equals("list")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            sendOpList(sender);
            return;
        }

        if (sub.equals("op")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Usage: /logs op <player>"));
                return;
            }
            ProxiedPlayer target = plugin.getProxy().getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Player not found: " + args[1]));
                return;
            }
            opManager.markOp(target.getUniqueId(), target.getName(), "manual");
            sender.sendMessage(new TextComponent(ChatColor.GREEN + "Marked " + args[1] + " as OP."));
            return;
        }

        if (sub.equals("unop")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Usage: /logs unop <player>"));
                return;
            }
            ProxiedPlayer target = plugin.getProxy().getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(new TextComponent(ChatColor.RED + "Player not found: " + args[1]));
                return;
            }
            opManager.unmarkOp(target.getUniqueId(), target.getName());
            sender.sendMessage(new TextComponent(ChatColor.GREEN + "Unmarked " + args[1] + " as OP."));
            return;
        }

        if (sub.equals("debug") || sub.equals("status")) {
            if (!canReload(sender)) { noPerm(sender); return; }
            if (args.length < 2) {
                sender.sendMessage(new TextComponent(ChatColor.RED
                        + "Usage: /logs " + sub + " <player>"));
                return;
            }
            ProxiedPlayer target = plugin.getProxy().getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(new TextComponent(ChatColor.RED
                        + "Player not found: " + args[1]));
                return;
            }
            String report = permChecker.explain(target);
            for (String line : report.split("\n")) {
                sender.sendMessage(new TextComponent(ChatColor.GRAY + line));
            }
            return;
        }

        sendHelp(sender);
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

        if (!isAdmin && !isUser) {
            noPerm(sender);
            return;
        }

        header(sender, "BungeeLogs - BungeeCord Commands");

        sender.sendMessage(new TextComponent(ChatColor.YELLOW + "General Commands"));
        row(sender, "/logs help", "Show this help");

        if (isUser) {
            row(sender, "/logs info", "Show plugin info");
            row(sender, "/logs creator", "Show plugin credits");
        }

        if (isAdmin) {
            separator(sender);
            sender.sendMessage(new TextComponent(ChatColor.RED + "Admin Commands"));
            row(sender, "/logs reload", "Reload config");
            row(sender, "/logs list", "List tracked OPs");
            row(sender, "/logs op <player>", "Manually mark OP");
            row(sender, "/logs unop <player>", "Manually unmark OP");
            row(sender, "/logs debug <player>", "Diagnose player");
            row(sender, "/logs status <player>", "Same as debug");
        }

        separator(sender);
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Channel: "
                + ChatColor.YELLOW + config.getChannel()));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Tracked OPs: "
                + ChatColor.YELLOW + opManager.getOpCount()));
        separator(sender);
    }

    private void sendInfo(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "BungeeLogs "
                + ChatColor.YELLOW + "v" + plugin.getDescription().getVersion()
                + ChatColor.AQUA + " by muvixo"));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Channel: "
                + ChatColor.WHITE + config.getChannel()));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Tracked OPs: "
                + ChatColor.WHITE + opManager.getOpCount()));
    }

    private void sendCreator(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "BungeeLogs "
                + ChatColor.YELLOW + "v" + plugin.getDescription().getVersion()));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "Author: "
                + ChatColor.AQUA + "muvixo"));
        sender.sendMessage(new TextComponent(ChatColor.GRAY + "API: "
                + ChatColor.WHITE + "BungeeCord 1.8+"));
    }

    private void sendOpList(CommandSender sender) {
        Map<UUID, OpPlayerManager.OpRecord> ops = opManager.getOpPlayers();
        header(sender, "Tracked OPs (" + ops.size() + ")");

        if (ops.isEmpty()) {
            sender.sendMessage(new TextComponent(ChatColor.GRAY + "  (none)"));
            separator(sender);
            return;
        }

        long now = System.currentTimeMillis();
        for (OpPlayerManager.OpRecord r : ops.values()) {
            long ageSec = (now - r.lastSeen) / 1000;
            String line = String.format("  %s | server=%s | lastSeen=%ds ago",
                    r.name, r.serverName, ageSec);
            sender.sendMessage(new TextComponent(ChatColor.GRAY + line));
        }
        separator(sender);
    }

    private void header(CommandSender sender, String title) {
        separator(sender);
        sender.sendMessage(new TextComponent(ChatColor.GOLD + title));
        separator(sender);
    }

    private void separator(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.DARK_GRAY
                + "----------------------------------"));
    }

    private void row(CommandSender sender, String cmd, String desc) {
        sender.sendMessage(new TextComponent(ChatColor.GOLD + "  " + cmd
                + ChatColor.GRAY + " - " + desc));
    }

    private void noPerm(CommandSender sender) {
        sender.sendMessage(new TextComponent(ChatColor.translateAlternateColorCodes('&',
                config.getNoPermissionMessage())));
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

            if (isUser) {
                subs.add("info");
                subs.add("creator");
            }
            if (isAdmin) {
                subs.add("reload");
                subs.add("list");
                subs.add("op");
                subs.add("unop");
                subs.add("debug");
                subs.add("status");
            }

            String partial = args.length == 0 ? "" : args[0].toLowerCase();
            for (String s : subs) if (s.startsWith(partial)) out.add(s);
            return out;
        }

        if (args.length == 2) {
            String sub = args[0].toLowerCase();
            if ((sub.equals("debug") || sub.equals("status")
                    || sub.equals("op") || sub.equals("unop"))
                    && canReload(sender)) {
                String partial = args[1].toLowerCase();
                for (ProxiedPlayer p : plugin.getProxy().getPlayers()) {
                    if (p.getName().toLowerCase().startsWith(partial)) {
                        out.add(p.getName());
                    }
                }
            }
        }
        return out;
    }
}
