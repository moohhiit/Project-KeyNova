package com.example.keynova

import android.content.Context
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity


class NameActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_name)

        val nameInput = findViewById<EditText>(R.id.editUserName)
        val saveButton = findViewById<Button>(R.id.buttonSaveName)

        saveButton.setOnClickListener {
            val name = nameInput.text.toString().trim()
            if (name.isNotEmpty()) {
                val prefs = getSharedPreferences("MyKeyboardPrefs", Context.MODE_PRIVATE)
                prefs.edit().putString("user_name", name).apply()
                Toast.makeText(this, "Name saved!", Toast.LENGTH_SHORT).show()
                finish() // go back to keyboard
            } else {
                Toast.makeText(this, "Please enter a name", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
