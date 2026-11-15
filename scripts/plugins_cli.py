#!/usr/bin/env python3
"""
Plugin CLI - Command Line Interface for Plugin Manager

Commands:
    plugins install <plugin_path> [--skip-governor]  - Install a plugin
    plugins list [--status STATUS]                   - List installed plugins
    plugins enable <plugin_key>                      - Enable/activate a plugin
    plugins disable <plugin_key>                     - Disable/deactivate a plugin
    plugins review <plugin_key> [--approve|--reject] - Review a plugin (Governor)
    plugins get <plugin_key>                         - Get plugin details
    plugins uninstall <plugin_key>                   - Uninstall a plugin
"""

import sys
import json
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Unicode glyphs (●/○/⟳/✗) crash on Windows cp1252 consoles unless stdout is UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:  # Python < 3.7
    pass

from plugins.manager import PluginManager


def cmd_install(args):
    """Install a plugin from a manifest.json or plugin directory."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    result = manager.install_plugin(args.plugin_path, skip_governor=args.skip_governor)
    if result.get("success"):
        print(f"✓ Installed: {result['plugin_key']}")
        if result.get("requires_governor_review"):
            print("  ⚠ Requires Governor review before activation")
    else:
        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


def cmd_list(args):
    """List installed plugins."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    plugins = manager.list_plugins(status=args.status)

    if args.json:
        print(json.dumps(plugins, indent=2))
        return

    if not plugins:
        print("No plugins found")
        return

    for plugin in plugins:
        status = plugin.get("status", "unknown")
        status_icon = {"active": "●", "inactive": "○", "pending_review": "⟳", "error": "✗"}.get(status, "?")
        print(f"{status_icon} {plugin['plugin_key']} ({status})")
        print(f"    {plugin['manifest'].get('name', '')} v{plugin['manifest'].get('version', '')}")
        print(f"    {plugin['manifest'].get('description', '')[:80]}")


def cmd_enable(args):
    """Enable/activate a plugin."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    result = manager.activate_plugin(args.plugin_key)
    if result.get("success"):
        print(f"✓ Enabled: {args.plugin_key}")
    else:
        print(f"✗ Failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)


def cmd_disable(args):
    """Disable/deactivate a plugin."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    plugin = manager.registry.get(args.plugin_key)
    if not plugin:
        print(f"Plugin not found: {args.plugin_key}")
        sys.exit(1)

    plugin.status = "inactive"
    manager._save_registry()
    print(f"✓ Disabled: {args.plugin_key}")


def cmd_review(args):
    """Review a plugin (Governor approval)."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    plugin = manager.registry.get(args.plugin_key)
    if not plugin:
        print(f"Plugin not found: {args.plugin_key}")
        sys.exit(1)

    if args.approve:
        plugin.status = "active"
        manager._log_audit_event({
            "event": "plugin_approved",
            "plugin_key": args.plugin_key,
            "approved_by": args.reviewer or "governor@vjsos-ai",
            "notes": args.notes or ""
        })
        manager._save_registry()
        print(f"✓ Approved and activated: {args.plugin_key}")
    elif args.reject:
        plugin.status = "rejected"
        manager._log_audit_event({
            "event": "plugin_rejected",
            "plugin_key": args.plugin_key,
            "rejected_by": args.reviewer or "governor@vjsos-ai",
            "notes": args.notes or ""
        })
        manager._save_registry()
        print(f"✗ Rejected: {args.plugin_key}")
    else:
        print(f"Plugin {args.plugin_key} status: {plugin.status}")
        print(f"  Manifest: {plugin.manifest}")


def cmd_get(args):
    """Get plugin details."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    plugin = manager.registry.get(args.plugin_key)
    if not plugin:
        print(f"Plugin not found: {args.plugin_key}")
        sys.exit(1)

    data = {
        "plugin_key": plugin.plugin_key,
        "status": plugin.status,
        "manifest": plugin.manifest,
        "config": plugin.config,
        "installed_at": plugin.installed_at,
        "audit_log": plugin.audit_log[-10:]  # Last 10 entries
    }
    print(json.dumps(data, indent=2, default=str))


def cmd_uninstall(args):
    """Uninstall a plugin."""
    manager = PluginManager(plugins_root=args.plugins_root, governor=None)
    plugin = manager.registry.get(args.plugin_key)
    if not plugin:
        print(f"Plugin not found: {args.plugin_key}")
        sys.exit(1)

    del manager.registry[args.plugin_key]
    manager._save_registry()
    print(f"✓ Uninstalled: {args.plugin_key}")


def main():
    parser = argparse.ArgumentParser(
        prog="plugins",
        description="VJSOS Plugin Manager CLI"
    )
    parser.add_argument("--plugins-root", default="plugins", help="Plugins root directory")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # install
    p_install = subparsers.add_parser("install", help="Install a plugin")
    p_install.add_argument("plugin_path", help="Path to manifest.json or plugin directory")
    p_install.add_argument("--skip-governor", action="store_true", help="Skip Governor review (dev only)")
    p_install.set_defaults(func=cmd_install)

    # list
    p_list = subparsers.add_parser("list", help="List installed plugins")
    p_list.add_argument("--status", choices=["active", "inactive", "pending_review", "error"], help="Filter by status")
    p_list.set_defaults(func=cmd_list)

    # enable
    p_enable = subparsers.add_parser("enable", help="Enable a plugin")
    p_enable.add_argument("plugin_key", help="Plugin key to enable")
    p_enable.set_defaults(func=cmd_enable)

    # disable
    p_disable = subparsers.add_parser("disable", help="Disable a plugin")
    p_disable.add_argument("plugin_key", help="Plugin key to disable")
    p_disable.set_defaults(func=cmd_disable)

    # review
    p_review = subparsers.add_parser("review", help="Review a plugin (Governor)")
    p_review.add_argument("plugin_key", help="Plugin key to review")
    p_review.add_argument("--approve", action="store_true", help="Approve the plugin")
    p_review.add_argument("--reject", action="store_true", help="Reject the plugin")
    p_review.add_argument("--reviewer", help="Reviewer identity")
    p_review.add_argument("--notes", help="Review notes")
    p_review.set_defaults(func=cmd_review)

    # get
    p_get = subparsers.add_parser("get", help="Get plugin details")
    p_get.add_argument("plugin_key", help="Plugin key")
    p_get.set_defaults(func=cmd_get)

    # uninstall
    p_uninstall = subparsers.add_parser("uninstall", help="Uninstall a plugin")
    p_uninstall.add_argument("plugin_key", help="Plugin key to uninstall")
    p_uninstall.set_defaults(func=cmd_uninstall)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()