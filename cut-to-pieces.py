# -*- coding: utf-8 -*-
from gimpfu import *
import gimp


def paths_to_images(image, drawable, path):
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)

    cnt, vectors = pdb.gimp_image_get_vectors(image)

    if cnt > 0:
        cnt = 0

        for id in vectors:
            vector = gimp.Vectors.from_id(id)
            pdb.gimp_vectors_to_selection(vector, 2, 1, 0, 0, 0)

            if pdb.gimp_edit_copy(drawable):
                new_image = pdb.gimp_edit_paste_as_new()

                pdb.gimp_file_save(
                    new_image,
                    pdb.gimp_image_get_active_drawable(new_image),
                    "%s/piece.%s.png" % (path, cnt),
                    "%s/piece.%s.png" % (path, cnt)
                )

                pdb.gimp_image_delete(new_image)
                cnt += 1

        pdb.gimp_selection_none(image)

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_context_pop()

register(
    'python-fu-cut-to-pieces',
    'Cut image by closed paths',
    'Cut image into pieces by closed paths',
    'Arthur Bikmullin',
    'Arthur Bikmullin aka devolonter',
    '17/02/2014',
    '<Image>/Filters/Paths/Cut to pieces...',
    '*',
    [
        (PF_DIRNAME, "path", "Save images here", ".")
    ],
    [],
    paths_to_images
)

main()