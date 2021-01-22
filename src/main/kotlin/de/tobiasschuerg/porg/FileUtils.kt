package de.tobiasschuerg.porg

import com.drew.imaging.ImageMetadataReader
import com.drew.imaging.quicktime.QuickTimeMetadataReader
import com.drew.metadata.exif.ExifSubIFDDirectory
import com.drew.metadata.mov.media.QuickTimeVideoDirectory
import com.drew.metadata.mp4.Mp4Directory
import java.io.File
import java.time.LocalDate

fun File.listAllFilesRecursively(): List<File> {
    return if (isDirectory) {
        listFiles().flatMap { it.listAllFilesRecursively() }
    } else {
        listOf(this)
    }
}

fun File.getDate(): LocalDate? {
    return when (extension.toLowerCase()) {
        "json" -> {
            println("Delete json file $this")
            this.delete()
            null
        }
        "jpg" -> {
            val metaData = ImageMetadataReader.readMetadata(this)
            val exifDir = metaData.getFirstDirectoryOfType(ExifSubIFDDirectory::class.java)
            if (exifDir != null) {
                getExifDate(exifDir)
            } else {
                println("No exif $this")
                null
            }
        }
        "mp4" -> {
            val metaData = ImageMetadataReader.readMetadata(this)
            getMp4Date(metaData.getFirstDirectoryOfType(Mp4Directory::class.java))
        }
        "mov" -> {
            val metaData = QuickTimeMetadataReader.readMetadata(this)
            val directory = metaData.getFirstDirectoryOfType(QuickTimeVideoDirectory::class.java)
            directory.getDate(QuickTimeVideoDirectory.TAG_CREATION_TIME)?.toLocalDate()
        }
        else -> {
            println("Unknown extension ${this.extension}")
            null
        }
    }
}

private fun getMp4Date(mp4: Mp4Directory): LocalDate {
    return mp4.getDate(Mp4Directory.TAG_CREATION_TIME).toLocalDate()
}

private fun getExifDate(exif: ExifSubIFDDirectory): LocalDate? {
    return exif.dateOriginal?.toLocalDate()
}