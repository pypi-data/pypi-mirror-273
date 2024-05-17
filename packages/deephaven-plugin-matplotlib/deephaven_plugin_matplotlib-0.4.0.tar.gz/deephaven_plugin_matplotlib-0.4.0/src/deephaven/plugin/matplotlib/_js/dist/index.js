"use strict";
const plugin = require("@deephaven/plugin");
const icons = require("@deephaven/icons");
const require$$1 = require("react");
const jsapiBootstrap = require("@deephaven/jsapi-bootstrap");
const Log = require("@deephaven/log");
var jsxRuntimeExports = {};
var jsxRuntime = {
  get exports() {
    return jsxRuntimeExports;
  },
  set exports(v) {
    jsxRuntimeExports = v;
  }
};
var reactJsxRuntime_production_min = {};
/*
object-assign
(c) Sindre Sorhus
@license MIT
*/
var getOwnPropertySymbols = Object.getOwnPropertySymbols;
var hasOwnProperty = Object.prototype.hasOwnProperty;
var propIsEnumerable = Object.prototype.propertyIsEnumerable;
function toObject(val) {
  if (val === null || val === void 0) {
    throw new TypeError("Object.assign cannot be called with null or undefined");
  }
  return Object(val);
}
function shouldUseNative() {
  try {
    if (!Object.assign) {
      return false;
    }
    var test1 = new String("abc");
    test1[5] = "de";
    if (Object.getOwnPropertyNames(test1)[0] === "5") {
      return false;
    }
    var test2 = {};
    for (var i = 0; i < 10; i++) {
      test2["_" + String.fromCharCode(i)] = i;
    }
    var order2 = Object.getOwnPropertyNames(test2).map(function(n2) {
      return test2[n2];
    });
    if (order2.join("") !== "0123456789") {
      return false;
    }
    var test3 = {};
    "abcdefghijklmnopqrst".split("").forEach(function(letter) {
      test3[letter] = letter;
    });
    if (Object.keys(Object.assign({}, test3)).join("") !== "abcdefghijklmnopqrst") {
      return false;
    }
    return true;
  } catch (err) {
    return false;
  }
}
shouldUseNative() ? Object.assign : function(target, source) {
  var from;
  var to = toObject(target);
  var symbols;
  for (var s = 1; s < arguments.length; s++) {
    from = Object(arguments[s]);
    for (var key in from) {
      if (hasOwnProperty.call(from, key)) {
        to[key] = from[key];
      }
    }
    if (getOwnPropertySymbols) {
      symbols = getOwnPropertySymbols(from);
      for (var i = 0; i < symbols.length; i++) {
        if (propIsEnumerable.call(from, symbols[i])) {
          to[symbols[i]] = from[symbols[i]];
        }
      }
    }
  }
  return to;
};
/** @license React v17.0.2
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var f = require$$1, g = 60103;
reactJsxRuntime_production_min.Fragment = 60107;
if ("function" === typeof Symbol && Symbol.for) {
  var h = Symbol.for;
  g = h("react.element");
  reactJsxRuntime_production_min.Fragment = h("react.fragment");
}
var m = f.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, n = Object.prototype.hasOwnProperty, p = { key: true, ref: true, __self: true, __source: true };
function q(c, a, k) {
  var b, d = {}, e = null, l = null;
  void 0 !== k && (e = "" + k);
  void 0 !== a.key && (e = "" + a.key);
  void 0 !== a.ref && (l = a.ref);
  for (b in a)
    n.call(a, b) && !p.hasOwnProperty(b) && (d[b] = a[b]);
  if (c && c.defaultProps)
    for (b in a = c.defaultProps, a)
      void 0 === d[b] && (d[b] = a[b]);
  return { $$typeof: g, type: c, key: e, ref: l, props: d, _owner: m.current };
}
reactJsxRuntime_production_min.jsx = q;
reactJsxRuntime_production_min.jsxs = q;
(function(module2) {
  {
    module2.exports = reactJsxRuntime_production_min;
  }
})(jsxRuntime);
const log = Log.module("@deephaven/js-plugin-matplotlib.MatplotlibView");
const MatplotlibViewStyle = {
  height: "100%",
  width: "100%",
  display: "contents"
};
const MatplotlibViewImageStyle = {
  height: "100%",
  width: "100%",
  objectFit: "contain"
};
function MatplotlibView(props) {
  const { fetch } = props;
  const [imageSrc, setImageSrc] = require$$1.useState();
  const [inputTable, setInputTable] = require$$1.useState();
  const [revision, setRevision] = require$$1.useState(0);
  const dh = jsapiBootstrap.useApi();
  require$$1.useEffect(
    function initInputTable() {
      if (!inputTable) {
        return;
      }
      const table = inputTable;
      async function openTable() {
        log.debug("openTable");
        const keyColumn = table.findColumn(
          "key"
          /* key */
        );
        const valueColumn = table.findColumn(
          "value"
          /* value */
        );
        table.applyFilter([
          keyColumn.filter().eq(dh.FilterValue.ofString(
            "revision"
            /* revision */
          ))
        ]);
        table.addEventListener(
          dh.Table.EVENT_UPDATED,
          ({ detail: data }) => {
            const newRevision = data.rows[0].get(valueColumn);
            log.debug("New revision", newRevision);
            setRevision(newRevision);
          }
        );
        table.setViewport(0, 0, [valueColumn]);
      }
      openTable();
      return function closeTable() {
        log.debug("closeTable");
        table.close();
      };
    },
    [dh, inputTable]
  );
  require$$1.useEffect(
    function updateData() {
      async function fetchData() {
        log.debug("fetchData");
        const widget = await fetch();
        const imageData = widget.getDataAsBase64();
        setImageSrc(`data:image/png;base64,${imageData}`);
        if (revision <= 0) {
          log.debug("Getting new input table");
          const newInputTable = await widget.exportedObjects[0].fetch();
          setInputTable(newInputTable);
        }
      }
      fetchData();
    },
    [fetch, revision]
  );
  return /* @__PURE__ */ jsxRuntimeExports.jsx("div", { className: "matplotlib-view", style: MatplotlibViewStyle, children: imageSrc !== void 0 && /* @__PURE__ */ jsxRuntimeExports.jsx(
    "img",
    {
      src: imageSrc,
      alt: "Matplotlib render",
      style: MatplotlibViewImageStyle
    }
  ) });
}
const MatplotlibPlugin = {
  name: "@deephaven/js-plugin-matplotlib",
  type: plugin.PluginType.WIDGET_PLUGIN,
  supportedTypes: "matplotlib.figure.Figure",
  component: MatplotlibView,
  icon: icons.vsGraph
};
module.exports = MatplotlibPlugin;
