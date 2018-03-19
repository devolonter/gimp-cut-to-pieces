# -*- coding: utf-8 -*-
from gimpfu import *
import gimp


def paths_to_images(image, drawable, path):
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)

    cnt, vectors = pdb.gimp_image_get_vectors(image)

    i = 0
    
    max_width = 0
    max_height = 0

    for id in vectors:
        vector = gimp.Vectors.from_id(id)
        pdb.gimp_image_select_item(image, 2, vector)
        pdb.gimp_edit_stroke(drawable)
        e, x1, y1, x2, y2 = pdb.gimp_selection_bounds(image)
        width = x2 - x1
        height = y2 - y1
        if e and width > max_width:
            max_width = width
        if e and height > max_height:
            max_height = height
    for id in vectors:
        vector = gimp.Vectors.from_id(id)
        pdb.gimp_vectors_to_selection(vector, 2, 1, 0, 0, 0)
        if pdb.gimp_edit_copy(drawable):
            new_image = pdb.gimp_image_new(max_width, max_height, 0)
            new_layer = pdb.gimp_layer_new(
                new_image,
                max_width,
                max_height,
                1,
                'main',
                0.0,
                0,
            )
            new_image.add_layer(new_layer, 0)
            pdb.gimp_edit_paste(new_layer, True)
            sel = pdb.gimp_image_get_floating_sel(new_image)
            # pdb.gimp_message(sel)
            pdb.gimp_floating_sel_anchor(sel)
            pdb.gimp_file_save(
                new_image,
                pdb.gimp_image_get_active_drawable(new_image),
                "%s/piece_%s.png" % (path, i),
                "%s/piece_%s.png" % (path, i)
            )

            pdb.gimp_image_delete(new_image)
            i += 1

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
