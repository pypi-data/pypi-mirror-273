const p = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], b = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
p.reduce(
  (f, { color: e, primary: a, secondary: n }) => ({
    ...f,
    [e]: {
      primary: b[e][a],
      secondary: b[e][n]
    }
  }),
  {}
);
const { setContext: Z, getContext: h } = window.__gradio__svelte__internal, w = "WORKER_PROXY_CONTEXT_KEY";
function v() {
  return h(w);
}
function k(f) {
  return f.host === window.location.host || f.host === "localhost:7860" || f.host === "127.0.0.1:7860" || // Ref: https://github.com/gradio-app/gradio/blob/v3.32.0/js/app/src/Index.svelte#L194
  f.host === "lite.local";
}
function C(f, e) {
  const a = e.toLowerCase();
  for (const [n, c] of Object.entries(f))
    if (n.toLowerCase() === a)
      return c;
}
function R(f) {
  if (f == null)
    return !1;
  const e = new URL(f, window.location.href);
  return !(!k(e) || e.protocol !== "http:" && e.protocol !== "https:");
}
async function E(f) {
  if (f == null || !R(f))
    return f;
  const e = v();
  if (e == null)
    return f;
  const n = new URL(f, window.location.href).pathname;
  return e.httpRequest({
    method: "GET",
    path: n,
    headers: {},
    query_string: ""
  }).then((c) => {
    if (c.status !== 200)
      throw new Error(`Failed to get file ${n} from the Wasm worker.`);
    const r = new Blob([c.body], {
      type: C(c.headers, "content-type")
    });
    return URL.createObjectURL(r);
  });
}
const {
  SvelteComponent: O,
  assign: i,
  compute_rest_props: _,
  detach: q,
  element: L,
  exclude_internal_props: U,
  get_spread_update: x,
  init: K,
  insert: T,
  noop: m,
  safe_not_equal: W,
  set_attributes: y,
  src_url_equal: X,
  toggle_class: g
} = window.__gradio__svelte__internal;
function Y(f) {
  let e, a, n = [
    {
      src: a = /*resolved_src*/
      f[0]
    },
    /*$$restProps*/
    f[1]
  ], c = {};
  for (let r = 0; r < n.length; r += 1)
    c = i(c, n[r]);
  return {
    c() {
      e = L("img"), y(e, c), g(e, "svelte-kxeri3", !0);
    },
    m(r, t) {
      T(r, e, t);
    },
    p(r, [t]) {
      y(e, c = x(n, [
        t & /*resolved_src*/
        1 && !X(e.src, a = /*resolved_src*/
        r[0]) && { src: a },
        t & /*$$restProps*/
        2 && /*$$restProps*/
        r[1]
      ])), g(e, "svelte-kxeri3", !0);
    },
    i: m,
    o: m,
    d(r) {
      r && q(e);
    }
  };
}
function P(f, e, a) {
  const n = ["src"];
  let c = _(e, n), { src: r = void 0 } = e, t, o;
  return f.$$set = (d) => {
    e = i(i({}, e), U(d)), a(1, c = _(e, n)), "src" in d && a(2, r = d.src);
  }, f.$$.update = () => {
    if (f.$$.dirty & /*src, latest_src*/
    12) {
      a(0, t = r), a(3, o = r);
      const d = r;
      E(d).then((s) => {
        o === d && a(0, t = s);
      });
    }
  }, [t, c, r, o];
}
class S extends O {
  constructor(e) {
    super(), K(this, e, P, Y, W, { src: 2 });
  }
}
new Intl.Collator(0, { numeric: 1 }).compare;
const {
  SvelteComponent: j,
  attr: I,
  create_component: N,
  destroy_component: z,
  detach: B,
  element: F,
  init: G,
  insert: H,
  mount_component: V,
  safe_not_equal: A,
  toggle_class: l,
  transition_in: D,
  transition_out: J
} = window.__gradio__svelte__internal;
function M(f) {
  var c, r;
  let e, a, n;
  return a = new S({
    props: {
      src: (
        /*value*/
        ((c = f[0].composite) == null ? void 0 : c.url) || /*value*/
        ((r = f[0].background) == null ? void 0 : r.url)
      ),
      alt: ""
    }
  }), {
    c() {
      e = F("div"), N(a.$$.fragment), I(e, "class", "container svelte-7kb74g"), l(
        e,
        "table",
        /*type*/
        f[1] === "table"
      ), l(
        e,
        "gallery",
        /*type*/
        f[1] === "gallery"
      ), l(
        e,
        "selected",
        /*selected*/
        f[2]
      );
    },
    m(t, o) {
      H(t, e, o), V(a, e, null), n = !0;
    },
    p(t, [o]) {
      var s, u;
      const d = {};
      o & /*value*/
      1 && (d.src = /*value*/
      ((s = t[0].composite) == null ? void 0 : s.url) || /*value*/
      ((u = t[0].background) == null ? void 0 : u.url)), a.$set(d), (!n || o & /*type*/
      2) && l(
        e,
        "table",
        /*type*/
        t[1] === "table"
      ), (!n || o & /*type*/
      2) && l(
        e,
        "gallery",
        /*type*/
        t[1] === "gallery"
      ), (!n || o & /*selected*/
      4) && l(
        e,
        "selected",
        /*selected*/
        t[2]
      );
    },
    i(t) {
      n || (D(a.$$.fragment, t), n = !0);
    },
    o(t) {
      J(a.$$.fragment, t), n = !1;
    },
    d(t) {
      t && B(e), z(a);
    }
  };
}
function Q(f, e, a) {
  let { value: n } = e, { type: c } = e, { selected: r = !1 } = e;
  return f.$$set = (t) => {
    "value" in t && a(0, n = t.value), "type" in t && a(1, c = t.type), "selected" in t && a(2, r = t.selected);
  }, [n, c, r];
}
class $ extends j {
  constructor(e) {
    super(), G(this, e, Q, M, A, { value: 0, type: 1, selected: 2 });
  }
}
export {
  $ as default
};
