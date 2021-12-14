package de.tobiasschuerg.porg

import com.drew.imaging.ImageMetadataReader
import com.drew.imaging.ImageProcessingException
import com.drew.imaging.quicktime.QuickTimeMetadataReader
import com.drew.metadata.Metadata
import com.drew.metadata.exif.ExifSubIFDDirectory
import com.drew.metadata.mov.media.QuickTimeVideoDirectory
import com.drew.metadata.mp4.Mp4Directory
import java.io.File
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.DateTimeParseException

fun File.listAllFilesRecursively(): List<File> {
    return if (isDirectory) {
        listFiles().flatMap { it.listAllFilesRecursively() }
    } else {
        listOf(this)
    }
}

fun File.listAllDirectoriesRecursively(): List<File> {
    return if (isDirectory) {
        val subDirectories = listFiles().flatMap { it.listAllDirectoriesRecursively() }
        listOf(this).plus(subDirectories)
    } else {
        emptyList()
    }
}

fun File.getDate(): LocalDate? {
    return when (extension.toLowerCase()) {
        "json" -> {
            println("Delete json file $this")
            this.delete()
            null
        }
        "jpg", "jpeg" -> {
            val metaData = ImageMetadataReader.readMetadata(this)
            val exifDir = metaData.getFirstDirectoryOfType(ExifSubIFDDirectory::class.java)
            if (exifDir != null) {
                getExifDate(exifDir)
            } else {
                val dateFromFilename = this.parseDateFromFilename()
                if (dateFromFilename != null) {
                    println("Parsing filename successful: $dateFromFilename")
                    dateFromFilename
                } else {
                    println("No exif $this")
                    null
                }
            }
        }
        "mp4" -> {
            try {
                val metaData: Metadata = ImageMetadataReader.readMetadata(this)
                val mp4: Mp4Directory? = metaData.getFirstDirectoryOfType(Mp4Directory::class.java)
                mp4?.let { getMp4Date(it) }
            } catch (e: ImageProcessingException) {
                println("Error processing ${this.name}")
                e.printStackTrace()
                null
            }
        }
        "mov" -> {
            val metaData = QuickTimeMetadataReader.readMetadata(this)
            val directory: QuickTimeVideoDirectory? =
                metaData.getFirstDirectoryOfType(QuickTimeVideoDirectory::class.java)
            directory?.getDate(QuickTimeVideoDirectory.TAG_CREATION_TIME)?.toLocalDate()
        }
        else -> {
            println("Unknown extension ${this.extension}")
            null
        }
    }
}

fun File.parseDateFromFilename(): LocalDate? {
    return try {
        when {
            nameWithoutExtension.toLowerCase().startsWith("img_") -> {
                LocalDate.parse(nameWithoutExtension.subSequence(4, 12), DateTimeFormatter.ofPattern("yyyyMMdd"))
            }
            nameWithoutExtension.toLowerCase().startsWith("img-") -> {
                LocalDate.parse(nameWithoutExtension.subSequence(4, 12), DateTimeFormatter.ofPattern("yyyyMMdd"))
            }
            else -> null
        }
    } catch (e: DateTimeParseException) {
        null
    }
}

private fun getMp4Date(mp4: Mp4Directory): LocalDate {
    return mp4.getDate(Mp4Directory.TAG_CREATION_TIME).toLocalDate()
}

private fun getExifDate(exif: ExifSubIFDDirectory): LocalDate? {
    return exif.dateOriginal?.toLocalDate()
}