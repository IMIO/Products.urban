
def updateTitle(rubricterm, event):
    """
     Update title after each change
    """
    rubricterm.updateTitle()


def updateIdAndSort(rubricterm, event):
    """
     Update id after each change and re-sort the rubrics (if needed).
    """
    rubricterm.id = rubricterm.getNumber()
    folder = rubricterm.aq_parent
    sorted_ids = sorted(folder.objectIds())
    for index in range(len(sorted_ids)):
        rurbric_id = sorted_ids[index]
        if folder.getObjectPosition(rurbric_id) != index:
            folder.moveObject(rurbric_id, index)
