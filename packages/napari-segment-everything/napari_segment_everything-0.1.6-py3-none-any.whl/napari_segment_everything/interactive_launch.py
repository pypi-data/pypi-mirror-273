import napari
viewer = napari.Viewer()

from napari_segment_everything import segment_everything


stop =5

viewer.window.add_dock_widget(
    segment_everything.NapariSegmentEverything(viewer)
)
napari.run()

