package de.tobiasschuerg.porg

import com.diogonunes.jcolor.Ansi
import com.diogonunes.jcolor.Attribute
import java.io.File

object OptionHelper {
    fun help(args: Array<String>): Options {

        val inputPath = args.firstOrNull()
        val inputDirectory = if (inputPath != null) {
            File(inputPath)
        } else {
            printPrompt("Please enter the source directory:")
            val path = readLine()
            File(path)
        }
        if (!inputDirectory.isDirectory) {
            error("This is not a directory")
        } else {
            println("Directory exists")
            val srcFiles = inputDirectory.listAllFilesRecursively()
            val directory = inputDirectory.listAllDirectoriesRecursively().count()
            val files = srcFiles.count { it.isFile }
            println("Source directory $inputDirectory contains $files files in $directory directories")
        }

        val outputPath = args.getOrNull(1)
        val outputDirectoy = if (outputPath != null) {
            File(outputPath)
        } else {
            println("Please enter the target directory:")
            val path = readLine()
            File(path)
        }
        println("output dir: $outputDirectoy")
        if (!outputDirectoy.exists()) {
            println("Does not exist an will be created")
            print("Press return to confirm")
            readLine()
        }

        return Options(inputDirectory, outputDirectoy, true)
    }
}