import textwrap


PAGE_WIDTH = 595
PAGE_HEIGHT = 842
BACKGROUND = (0.059, 0.067, 0.082)
CARD_BACKGROUND = (0.086, 0.105, 0.133)
PRIMARY = (0.902, 0.929, 0.953)
SECONDARY = (0.545, 0.592, 0.635)
ACCENT = (0.824, 0.631, 0.369)


def _pdf_string(value):
    return str(value).encode("cp1252", errors="replace").hex().upper()


def _text(commands, value, x, y, size, color, font="F1"):
    red, green, blue = color
    commands.append(
        f"BT /{font} {size} Tf {red:.3f} {green:.3f} {blue:.3f} rg "
        f"1 0 0 1 {x:.2f} {PAGE_HEIGHT - y:.2f} Tm <{_pdf_string(value)}> Tj ET"
    )


def _rectangle(commands, x, y, width, height, color):
    red, green, blue = color
    commands.append(
        f"{red:.3f} {green:.3f} {blue:.3f} rg "
        f"{x} {PAGE_HEIGHT - y - height} {width} {height} re f"
    )


def _new_page(commands, username, period, page_number):
    _rectangle(commands, 0, 0, PAGE_WIDTH, PAGE_HEIGHT, BACKGROUND)
    _rectangle(commands, 48, 38, 46, 46, CARD_BACKGROUND)
    _text(commands, "FM", 57, 67, 18, ACCENT, "F2")
    _text(commands, "FILMMANAGER", 108, 52, 9, ACCENT, "F2")
    _text(commands, "Estadísticas de tu colección", 108, 74, 17, PRIMARY, "F2")
    _text(commands, f"{username}  ·  {period}", 48, 112, 9, SECONDARY)
    _text(commands, f"{page_number}", 535, 810, 8, SECONDARY)


def generar_pdf_resumen(data, username, selected_year=None):
    period = str(selected_year) if selected_year else "Todos los años"
    pages = [[]]
    _new_page(pages[-1], username, period, 1)
    y = 148

    sections = (
        ("RESUMEN", (
            ("Películas y series vistas", data["peliculas_series_vistas"]),
            ("Favoritas", data["favoritas"]),
            ("Nota media global", data["nota_media_global"]),
            ("Tiempo total invertido", data["tiempo_invertido_total"]),
        )),
        ("PELÍCULAS", (
            ("Películas vistas", data["peliculas_vistas"]),
            ("Tiempo en películas", data["tiempo_invertido_peliculas"]),
            ("Nota media en películas", data["nota_media_peliculas"]),
            ("Película más larga", data["pelicula_mas_larga"]),
            ("Película más corta", data["pelicula_mas_corta"]),
            ("Top 3 mejores", data["top_mejores_peliculas"]),
            ("Top 3 peores", data["top_peores_peliculas"]),
        )),
        ("SERIES", (
            ("Series vistas", data["series_vistas"]),
            ("Tiempo en series", data["tiempo_invertido_series"]),
            ("Nota media en series", data["nota_media_series"]),
            ("Serie más larga", data["serie_mas_larga"]),
            ("Serie más corta", data["serie_mas_corta"]),
            ("Top 3 mejores", data["top_mejores_series"]),
            ("Top 3 peores", data["top_peores_series"]),
        )),
    )

    for title, rows in sections:
        if y > 700:
            pages.append([])
            _new_page(pages[-1], username, period, len(pages))
            y = 148

        _text(pages[-1], title, 48, y, 10, ACCENT, "F2")
        y += 15
        for label, value in rows:
            wrapped_value = textwrap.wrap(str(value), width=68) or [""]
            card_height = max(34, 18 + (len(wrapped_value) - 1) * 11)
            if y + card_height > 780:
                pages.append([])
                _new_page(pages[-1], username, period, len(pages))
                y = 148
                _text(pages[-1], title, 48, y, 10, ACCENT, "F2")
                y += 15

            _rectangle(pages[-1], 48, y, 499, card_height, CARD_BACKGROUND)
            _rectangle(pages[-1], 48, y, 3, card_height, ACCENT)
            _text(pages[-1], label, 62, y + 21, 8.5, SECONDARY)
            for line_number, line in enumerate(wrapped_value):
                _text(
                    pages[-1],
                    line,
                    226,
                    y + 16 + line_number * 11,
                    8.5,
                    PRIMARY,
                )
            y += card_height + 5
        y += 13

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [] /Count 0 >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    ]
    page_references = []
    for commands in pages:
        content = ("\n".join(commands)).encode("ascii")
        content_number = len(objects) + 1
        objects.append(
            b"<< /Length "
            + str(len(content)).encode("ascii")
            + b" >>\nstream\n"
            + content
            + b"\nendstream"
        )
        page_number = len(objects) + 1
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH} "
                f"{PAGE_HEIGHT}] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> "
                f">> /Contents {content_number} 0 R >>"
            ).encode("ascii")
        )
        page_references.append(f"{page_number} 0 R")

    objects[1] = (
        f"<< /Type /Pages /Kids [{' '.join(page_references)}] "
        f"/Count {len(page_references)} >>"
    ).encode("ascii")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{number} 0 obj\n".encode("ascii"))
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n"
        ).encode("ascii")
    )
    return bytes(pdf)
