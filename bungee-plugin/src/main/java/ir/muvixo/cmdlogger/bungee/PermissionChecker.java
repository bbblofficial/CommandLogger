package ir.muvixo.cmdlogger.bungee;

import net.md_5.bungee.api.connection.ProxiedPlayer;

/**
 * Central permission checker for BungeeCord.
 *
 * Created by Muvixo
 */
public class PermissionChecker {

    private final Config config;
    private final OpPlayerManager opManager;

    public PermissionChecker(Config config, OpPlayerManager opManager, CommandLogger plugin) {
        this.config = config;
        this.opManager = opManager;
    }

    public boolean canSee(ProxiedPlayer player) {
        if (player == null) return false;

        if (opManager.isOp(player.getUniqueId())) return true;

        String seePerm = config.getSeePermission();
        String adminPerm = config.getAdminPermission();
        if (seePerm != null && !seePerm.isEmpty() && player.hasPermission(seePerm)) return true;
        if (adminPerm != null && !adminPerm.isEmpty() && player.hasPermission(adminPerm)) return true;

        return false;
    }

    public boolean canReload(ProxiedPlayer player) {
        if (player == null) return false;
        String adminPerm = config.getAdminPermission();
        if (adminPerm != null && !adminPerm.isEmpty() && player.hasPermission(adminPerm)) return true;
        return opManager.isOp(player.getUniqueId());
    }

    public String explain(ProxiedPlayer player) {
        String seePerm = config.getSeePermission();
        String adminPerm = config.getAdminPermission();
        StringBuilder sb = new StringBuilder();
        sb.append("Player: ").append(player.getName())
          .append(" (").append(player.getUniqueId()).append(")\n");
        sb.append("  tracked-as-op: ").append(opManager.isOp(player.getUniqueId())).append("\n");
        sb.append("  op-server: ").append(opManager.getOpServer(player.getUniqueId())).append("\n");
        sb.append("  has ").append(seePerm).append(": ")
          .append(player.hasPermission(seePerm)).append("\n");
        sb.append("  has ").append(adminPerm).append(": ")
          .append(player.hasPermission(adminPerm)).append("\n");
        sb.append("  RESULT: ").append(canSee(player) ? "CAN SEE LOGS" : "CANNOT SEE LOGS");
        return sb.toString();
    }
}
