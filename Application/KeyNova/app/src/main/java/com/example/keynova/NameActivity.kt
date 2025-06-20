package com.example.keynova

import android.content.Context
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.keynova.data.api.RetrofitClient
import com.example.keynova.data.model.LoginRequest
import kotlinx.coroutines.*

class NameActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_name)


        val nameInput = findViewById<EditText>(R.id.editUserName)
        val saveButton = findViewById<Button>(R.id.buttonSaveName)
        val secret_key = findViewById<EditText>(R.id.passkey)

        saveButton.setOnClickListener {
            
        }

        fun loginUser(username: String, password: String) {
            CoroutineScope(Dispatchers.IO).launch {
                try {
                    // 1. Login
                    val loginResponse = RetrofitClient.apiService.login(LoginRequest(username, password))
                    val token = "Token ${loginResponse.auth_token}"

                    // 2. Get user data
                    val user = RetrofitClient.apiService.getUser(token)

                    // 3. Back to main thread (UI)
                    withContext(Dispatchers.Main) {
                        println("Welcome, ${user.username}")
                    }

                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
    }
}
