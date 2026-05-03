export function getPrefix(url: URL): string {
  const base = import.meta.env.BASE_URL || "/";
  const baseWithoutTrailing = base.endsWith("/") ? base.slice(0, -1) : base;
  const pathAfterBase = url.pathname.slice(baseWithoutTrailing.length);
  const depth = pathAfterBase.split("/").filter(Boolean).length;
  return depth ? "../".repeat(depth) : "./";
}

export function navHref(prefix: string, path: string): string {
  if (path === "/") return prefix;
  return `${prefix}${path.replace(/^\//, "")}`;
}
