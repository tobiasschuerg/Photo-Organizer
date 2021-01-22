package de.tobiasschuerg.porg

import java.io.File

data class Options(
    val src: File,
    val target: File,
    val move: Boolean = false
)
