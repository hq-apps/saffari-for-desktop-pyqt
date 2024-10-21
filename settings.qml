import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: settingsWindow
    visible: true
    width: 400
    height: 300
    title: "Settings"

    Column {
        anchors.centerIn: parent

        Row {
            spacing: 10
            Label {
                text: "Home page:"
            }
            TextField {
                id: homepageField
                placeholderText: "Enter homepage URL"
                text: settingsManager.load_homepage()
            }
            Button {
                text: "Reset"
                onClicked: {
                    homepageField.text = ""
                    settingsManager.save_homepage("")
                }
            }
        }

        Button {
            text: "Save"
            onClicked: {
                settingsManager.save_homepage(homepageField.text)
            }
        }

        // Close button to hide the settings window
        Button {
            text: "Close"
            onClicked: {
                settingsWindow.close()
            }
        }

        // Exit button to close the entire application
        Button {
            text: "Exit"
            highlighted: true
            onClicked: {
                Qt.quit()
            }
        }
    }
}
