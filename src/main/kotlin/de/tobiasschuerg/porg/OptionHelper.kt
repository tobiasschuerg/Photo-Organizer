package de.tobiasschuerg.porg

import java.io.File
import kotlin.system.exitProcess

object OptionHelper {
    fun help(args: Array<String>): Options {

        val inputPath = args.firstOrNull()
        val inputDirectory = if (inputPath != null) {
            File(inputPath)
        } else {
            println("Please enter the source directory:")
            val path = readLine()
            File(path)
        }
        if (!inputDirectory.isDirectory) {
            error("This is not a directory")
        } else {
            println("Directory exists")
            val srcFiles = inputDirectory.listAllFilesRecursively()
            val directory = srcFiles.filter { it.isDirectory }.count()
            val files = srcFiles.filter { it.isFile }.count()
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
        println("output dir: $outputPath")
        if (!outputDirectoy.exists()) {
            println("Does not exist an will be created")
            print("Press return to confirm")
            readLine()
        }

        return Options(inputDirectory, outputDirectoy, true)
    }
}