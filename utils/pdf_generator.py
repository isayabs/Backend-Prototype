def generate_pdf(title, df, filename):
    folder = "static/pdf/"
    path = folder + filename

    with open(path, "w") as f:
        f.write(title + "\n\n")
        f.write(df.to_string())

    return path