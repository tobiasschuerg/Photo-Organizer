package de.tobiasschuerg.porg

import com.diogonunes.jcolor.Ansi
import com.diogonunes.jcolor.Attribute

fun printPrompt(message: String) {
    println(Ansi.colorize(message, Attribute.BLUE_TEXT()))
}