var inject = function () {
  let config = {
    "random": {
      "value": function () {
        return Math.random();
      },
      "item": function (e) {
        let rand = e.length * config.random.value();
        return e[Math.floor(rand)];
      },
      "number": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          tmp.push(Math.pow(2, power[i]));
        }
        /*  */
        return config.random.item(tmp);
      },
      "int": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          let n = Math.pow(2, power[i]);
          tmp.push(new Int32Array([n, n]));
        }
        /*  */
        return config.random.item(tmp);
      },
      "float": function (power) {
        let tmp = [];
        for (let i = 0; i < power.length; i++) {
          let n = Math.pow(2, power[i]);
          tmp.push(new Float32Array([1, n]));
        }
        /*  */
        return config.random.item(tmp);
      }
    },
    "spoof": {
      "webgl": {
        "buffer": function (target) {
          let proto = target.prototype ? target.prototype : target.__proto__;
          //
          proto.bufferData = new Proxy(proto.bufferData, {
            apply(target, self, args) {
              let index = Math.floor(config.random.value() * args[1].length);
              let noise = args[1][index] !== undefined ? 0.1 * config.random.value() * args[1][index] : 0;
              //
              args[1][index] = args[1][index] + noise;
              console.debug("webgl-fingerprint-defender-alert");
              //
              return Reflect.apply(target, self, args);
            }
          });
        },
        "parameter": function (target) {
          let proto = target.prototype ? target.prototype : target.__proto__;
          //
          proto.getParameter = new Proxy(proto.getParameter, {
            apply(target, self, args) {
              console.debug("webgl: " + args)

              // Linux
              if (args[0] === 3415) return 0;
              else if (args[0] === 3414) return 24;
              else if (args[0] === 36348) return 32;
              else if (args[0] === 7936) return "Mozilla";
              else if (args[0] === 37445) return "AMD";
              else if (args[0] === 7937) return "Radeon R9 200 Series, or similar";
              else if (args[0] === 3379) return 16384;
              else if (args[0] === 36347) return 4096;
              else if (args[0] === 34076) return 16384;
              else if (args[0] === 34024) return 16384;
              else if (args[0] === 3386) return new Int32Array([16384, 16384]);
              else if (args[0] === 3413) return 8;
              else if (args[0] === 3412) return 8;
              else if (args[0] === 3411) return 8;
              else if (args[0] === 3410) return 8;
              else if (args[0] === 34047) return null;
              else if (args[0] === 34930) return 32;
              else if (args[0] === 34921) return 16;
              else if (args[0] === 35660) return 32;
              else if (args[0] === 35661) return 192;
              else if (args[0] === 36349) return 4096;
              else if (args[0] === 33902) return new Float32Array([1, 2048]);
              else if (args[0] === 33901) return new Float32Array([0.125, 2048]);
              else if (args[0] === 37446) return "Radeon R9 200 Series, or similar";
              else if (args[0] === 7938) return "WebGL 1.0";
              else if (args[0] === 35724) return "WebGL GLSL ES 1.0";

              // Windows
              if (args[0] === 3415) return 0;
              else if (args[0] === 3414) return 24;
              else if (args[0] === 36348) return 30;
              else if (args[0] === 7936) return "Mozilla";
              else if (args[0] === 37445) return "Google Inc. (NVIDIA)";
              else if (args[0] === 7937) return "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar";
              else if (args[0] === 3379) return 16384;
              else if (args[0] === 36347) return 4095;
              else if (args[0] === 34076) return 16384;
              else if (args[0] === 34024) return 16384;
              else if (args[0] === 3386) return new Int32Array([32767, 32767]);
              else if (args[0] === 3413) return 8;
              else if (args[0] === 3412) return 8;
              else if (args[0] === 3411) return 8;
              else if (args[0] === 3410) return 8;
              else if (args[0] === 34047) return null;
              else if (args[0] === 34930) return 16;
              else if (args[0] === 34921) return 16;
              else if (args[0] === 35660) return 16;
              else if (args[0] === 35661) return 32;
              else if (args[0] === 36349) return 1024;
              else if (args[0] === 33902) return new Float32Array([1, 1]);
              else if (args[0] === 33901) return new Float32Array([1, 1024]);
              else if (args[0] === 37446) return "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0), or similar";
              else if (args[0] === 7938) return "WebGL";
              else if (args[0] === 35724) return "WebGL GLSL ES 1.0";

              //
              return Reflect.apply(target, self, args);
            }
          });
        }
      }
    }
  };
  //
  config.spoof.webgl.buffer(WebGLRenderingContext);
  config.spoof.webgl.buffer(WebGL2RenderingContext);
  config.spoof.webgl.parameter(WebGLRenderingContext);
  config.spoof.webgl.parameter(WebGL2RenderingContext);
  //
  // Note: this variable is for targeting sandboxed iframes
  document.documentElement.dataset.wgscriptallow = true;
};

let script_1 = document.createElement("script");
script_1.textContent = "(" + inject + ")()";
document.documentElement.appendChild(script_1);
script_1.remove();

if (document.documentElement.dataset.wgscriptallow !== "true") {
  let script_2 = document.createElement("script");
  //
  script_2.textContent = `{
    const iframes = [...window.top.document.querySelectorAll("iframe[sandbox]")];
    for (let i = 0; i < iframes.length; i++) {
      if (iframes[i].contentWindow) {
        if (iframes[i].contentWindow.WebGLRenderingContext) {
          iframes[i].contentWindow.WebGLRenderingContext.prototype.bufferData = WebGLRenderingContext.prototype.bufferData;
          iframes[i].contentWindow.WebGLRenderingContext.prototype.getParameter = WebGLRenderingContext.prototype.getParameter;
        }
        //
        if (iframes[i].contentWindow.WebGL2RenderingContext) {
          iframes[i].contentWindow.WebGL2RenderingContext.prototype.bufferData = WebGL2RenderingContext.prototype.bufferData;
          iframes[i].contentWindow.WebGL2RenderingContext.prototype.getParameter = WebGL2RenderingContext.prototype.getParameter;
        }
      }
    }
  }`;
  //
  window.top.document.documentElement.appendChild(script_2);
  script_2.remove();
}
