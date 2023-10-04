import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.VirtualKeyboard 2.15
import QtQuick.VirtualKeyboard.Styles 2.15



Item {
    id: window
    x: 0
    y: 320
    
    
	
    Rectangle
    {
        id: background
	anchors.centerIn: parent
    	width: 1000
    	height: 1000
        color: "black"
    }

    InputPanel {
        id: inputPanel
        width: window.width
        height: window.height
	property var isKeyboardActive: inputPanel.active 
        objectName: "inputPanel_object"

        states: State {
            name: "visible"
            when: inputPanel.active
            PropertyChanges {
                target: window
                height: inputPanel.height
                y: window.height - inputPanel.height
            }
        }
        transitions: Transition {
            from: ""
            to: "visible"
            reversible: true
            ParallelAnimation {
                NumberAnimation {
                    properties: "y"
                    duration: 250
                    easing.type: Easing.InOutQuad
                }
            }
        }
    }
}

