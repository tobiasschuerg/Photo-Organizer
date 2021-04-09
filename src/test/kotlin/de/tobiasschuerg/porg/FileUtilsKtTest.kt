package de.tobiasschuerg.porg

import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.Test
import java.io.File
import java.time.LocalDate

internal class FileUtilsKtTest {

    @Test
    fun `test IMG_ date`(){
        val file = File("foo/bar/IMG_20160917_083309-01.jpeg")
        val date = file.parseDateFromFilename()
        assertEquals(LocalDate.of(2016, 9, 17), date)
    }

    @Test
    fun `test IMG- date`(){
        val file = File("foo/IMG-20180801-WA0006-bearbeitet.jpg")
        val date = file.parseDateFromFilename()
        assertEquals(LocalDate.of(2018, 8, 1), date)
    }


}