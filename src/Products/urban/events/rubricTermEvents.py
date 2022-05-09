from plone import api

def updateTitle(rubricterm, event):
    """
     Update title after each change
    """
    rubricterm.updateTitle()


def updateIdAndSort(rubricterm, event):
    """
     Update id after each change and re-sort the rubrics (if needed).
    """
    api.content.rename(obj=rubricterm, new_id=rubricterm.getNumber())
    folder = rubricterm.aq_parent
    sorted_ids = sorted(folder.objectIds())
    for index in range(len(sorted_ids)):
        rubric_id = sorted_ids[index]
        if folder.getObjectPosition(rubric_id) != index:
            folder.moveObject(rubric_id, index)
