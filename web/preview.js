import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

app.registerExtension({
    name: "KK.Mistune.Modern.Preview",
    beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "KKMistuneModern") return;

        const originalCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = originalCreated?.apply(this, arguments);
            const widget = ComfyWidgets.STRING(
                this,
                "转换结果",
                ["STRING", { multiline: true }],
                app
            ).widget;
            widget.inputEl.readOnly = true;
            widget.inputEl.style.opacity = "1";
            widget.value = "等待运行工作流";
            widget.options = { ...widget.options, serialize: false };
            widget.serialize = false;
            this.kkMistuneResultWidget = widget;
            this.setSize([Math.max(this.size[0], 380), Math.max(this.size[1], 300)]);
            return result;
        };

        const originalExecuted = nodeType.prototype.onExecuted;
        nodeType.prototype.onExecuted = function (message) {
            const result = originalExecuted?.apply(this, arguments);
            const values = message?.text;
            if (this.kkMistuneResultWidget && Array.isArray(values)) {
                this.kkMistuneResultWidget.value = values.join("\n");
                this.setDirtyCanvas(true, true);
            }
            return result;
        };
    },
});
