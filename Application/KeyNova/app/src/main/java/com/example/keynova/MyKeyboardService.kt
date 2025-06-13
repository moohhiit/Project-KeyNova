package com.example.keynova


import android.app.AlertDialog
import android.content.ClipboardManager
import android.content.Intent
import android.inputmethodservice.InputMethodService
import android.view.KeyEvent
import android.view.LayoutInflater
import android.view.View
import android.widget.Button
import android.widget.TextView

class MyKeyboardService : InputMethodService() {
    override fun onCreateInputView(): View {
        val inflater = LayoutInflater.from(this)
        val view = inflater.inflate(R.layout.keyboard_layout, null)

        val letters = listOf(
            "Q","W","E","R","T","Y","U","I","O","P",
            "A","S","D","F","G","H","J","K","L",
            "Z","X","C","V","B","N","M"
        )
        val userNameText = view.findViewById<TextView>(R.id.userNameText)
        val prefs = getSharedPreferences("MyKeyboardPrefs", MODE_PRIVATE)
        val userName = prefs.getString("user_name", "User")
        userNameText.text = "Hi, $userName!"


        for (letter in letters) {
            val id = resources.getIdentifier("button$letter", "id", packageName)
            val btn = view.findViewById<Button>(id)
            btn?.setOnClickListener {
                currentInputConnection.commitText(letter, 1)
            }
        }
        val settingsButton = view.findViewById<Button>(R.id.buttonSettings)
        settingsButton.setOnClickListener {
            // Open NameActivity using an intent
            val intent = Intent(this, NameActivity::class.java)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            startActivity(intent)
        }

        val clipboardButton = view.findViewById<Button>(R.id.buttonClipboard)
        clipboardButton.setOnClickListener {
            val clipboard = getSystemService(CLIPBOARD_SERVICE) as ClipboardManager
            val clipData = clipboard.primaryClip
            if (clipData != null && clipData.itemCount > 0) {
                val text = clipData.getItemAt(0).coerceToText(this).toString()
                ClipboardHistory.add(text)
                currentInputConnection.commitText(text, 1)
            }
        }


        val historyButton = view.findViewById<Button>(R.id.buttonHistory)
        historyButton.setOnClickListener {
            val builder = AlertDialog.Builder(this)
            builder.setTitle("Clipboard History")

            val items = ClipboardHistory.getAll().toTypedArray()
            builder.setItems(items) { _, which ->
                currentInputConnection.commitText(items[which], 1)
            }

            builder.setNegativeButton("Close", null)
            builder.show()
        }

        val space = view.findViewById<Button>(R.id.buttonSpace)
        space.setOnClickListener {
            currentInputConnection.commitText(" ", 1)
        }

        val delete = view.findViewById<Button>(R.id.buttonDelete)
        delete.setOnClickListener {
            currentInputConnection.deleteSurroundingText(1, 0)
        }


        val at = view.findViewById<Button>(R.id.buttonAt)
        at.setOnClickListener {
            currentInputConnection.commitText("@", 1)
        }

        val question = view.findViewById<Button>(R.id.buttonQuestion)
        question.setOnClickListener {
            currentInputConnection.commitText("?", 1)
        }

        val enter = view.findViewById<Button>(R.id.buttonEnter)
        enter.setOnClickListener {
            currentInputConnection.sendKeyEvent(
                KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_ENTER)
            )
        }


        return view
    }

}