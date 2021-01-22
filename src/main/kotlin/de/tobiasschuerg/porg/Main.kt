package de.tobiasschuerg.porg

import java.io.File
import java.nio.file.Files
import java.nio.file.Paths
import java.time.format.DateTimeFormatter


class Main {

    companion object {

        @JvmStatic
        fun main(args: Array<String>) {
            val options = OptionHelper.help(args)
            println("Source folder: ${options.src}")
            println("Target folder: ${options.target}")
            println("Move: ${options.move}")
            println("========== continue? ========")
            readLine()

            val listAllFilesRecursively = options.src.listAllFilesRecursively()
            listAllFilesRecursively
                .forEachIndexed { index, file ->
                    // print("$index $file")

                    val date = file.getDate()
                    if (date != null) {
                        println(" .. Date: $date")

                        val year = date.year
                        val month = date.format(DateTimeFormatter.ofPattern("MM"))
                        val day = date.format(DateTimeFormatter.ofPattern("dd"))

                        val filename = file.name
                        val targetFile = File(options.target, "$year/$year-$month-$day/$filename")

                        if (options.move) {
                            val filepath1 = Paths.get(file.toURI())
                            val targetpath1 = Paths.get(targetFile.toURI())
                            Files.createDirectories(targetpath1.parent)
                            Files.move(filepath1, targetpath1)
                        } else {
                            file.copyTo(targetFile, true)
                        }
                    } else {
                        println(" !!! Skipped $file, could not determine date")
                    }
                }
        }
    }
}
