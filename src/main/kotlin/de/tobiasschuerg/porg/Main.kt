package de.tobiasschuerg.porg

import java.io.File
import java.nio.file.Files
import java.nio.file.Paths
import java.time.format.DateTimeFormatter


class Main {

    companion object {
        val move = true

        @JvmStatic
        fun main(args: Array<String>) {
            args.forEach {
                println("Args: $it")
            }

            val inputPath = args.first()
            val inputDirectory = File(inputPath)
            println("input dir: $inputPath")

            val outputPath = args[1]
            val outputDirectoy = File(outputPath)
            println("output dir: $inputPath")

            val listAllFilesRecursively = inputDirectory.listAllFilesRecursively()
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
                        val targetFile = File(outputDirectoy, "$year/$year-$month-$day/$filename")

                        if (move) {
                            val filepath1 = Paths.get(file.toURI())
                            val targetpath1 = Paths.get(targetFile.toURI())
                            Files.createDirectories(targetpath1.parent)
                            Files.move(filepath1, targetpath1)
                        } else {
                            file.copyTo(targetFile, true)
                        }
                    } else {
//                        println(" !!! Skipped $file")
                    }
                }
        }
    }
}
