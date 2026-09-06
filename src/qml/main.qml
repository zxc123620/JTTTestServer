import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Layouts 1.15
import "components" as Components


Window {


    width: 800
    height: 600
    visible: true
    title: "EvolveUI 示例"

    // 导入主题
    Components.ETheme {
        id: theme
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20

        // 使用按钮组件
        Components.EButton {
            text: "点击我"
            iconCharacter: "\uf0a9"  // 手形图标
            onClicked: {
                // 显示消息提示
                toast.show("欢迎使用 EvolveUI!")
            }
        }

        // 使用输入框组件
        Components.EInput {
            placeholderText: "请输入您的姓名"
            Layout.preferredWidth: 300
        }

        // 使用开关按钮组件
        Components.ESwitchButton {
            text: "启用功能"
            checked: true
        }

        // 使用消息提示组件
        Components.EToast {
            id: toast
        }
    }
}