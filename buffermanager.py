from file import File

buffersize = 5
pages = []


def getPage(fileName, pageId):
    f = File(fileName)

    if not f.exists:
        raise Exception("File not found")

    p = f.loadPage(pageId)
    pages.append(p)

    if len(pages) > 5:
        pages.pop(0)
    return p

def updatePage(p, filename, pageId):
    f = File(filename)

    if not f.exists:
        raise Exception("File not found")

    if p.isEmpty() and p.deleted:
        f.deletePage(pageId)
        return
    f.updatePage(pageId, p)