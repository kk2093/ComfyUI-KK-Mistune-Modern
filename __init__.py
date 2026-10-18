"""仅用于依赖版本冲突演示的 ComfyUI 文本节点。"""


class KKMistuneModern:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING", {
                    "multiline": True,
                    "default": "你好，**ComfyUI**！",
                }),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("HTML文本", "依赖版本")
    FUNCTION = "convert"
    CATEGORY = "KK测试/依赖版本冲突"
    OUTPUT_NODE = True
    DESCRIPTION = "使用 Mistune 3.0.2 将 Markdown 文本转换为 HTML。"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 演示节点每次排队均执行，以便观察实际依赖及结果。
        return float("nan")

    def convert(self, 文本):
        # 执行时才导入及调用版本相关接口，不在注册节点时调用。
        import mistune

        markdown = mistune.create_markdown(escape=True)
        html = str(markdown(文本))
        version = str(mistune.__version__)
        report = "实际依赖：mistune " + version + "\n\n转换结果：\n" + html
        return {
            "ui": {"text": [report]},
            "result": (html, version),
        }


NODE_CLASS_MAPPINGS = {"KKMistuneModern": KKMistuneModern}
NODE_DISPLAY_NAME_MAPPINGS = {"KKMistuneModern": "新版文本转换（Mistune 3.0.2）"}
WEB_DIRECTORY = "./web"
