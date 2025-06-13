object ClipboardHistory {
    val items = mutableListOf<String>()

    fun add(text: String) {
        if (text.isNotBlank() && !items.contains(text)) {
            items.add(0, text)
            if (items.size > 5) items.removeAt(-1)
        }
    }

    fun getAll(): List<String> = items
}
