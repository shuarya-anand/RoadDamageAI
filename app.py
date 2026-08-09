"""RoadDamageAI desktop interface."""

import os
import sys
import threading
from collections import Counter

import cv2
import customtkinter as ctk
from PIL import Image, ImageOps
from ultralytics import YOLO


def resource_path(relative_path):
    """Get absolute path to resource, works for development and PyInstaller."""
    if getattr(sys, "frozen", False):
        # Running as a bundled executable
        base_path = os.path.dirname(sys.executable)
    else:
        # Running from source
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# ---------------------------------------------------------------------------
# Appearance
# ---------------------------------------------------------------------------

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

APP_BG = "#0B1120"
SURFACE = "#111C31"
SURFACE_ELEVATED = "#16233B"
BORDER = "#263653"
TEXT = "#F4F7FB"
MUTED = "#8EA0BD"

BLUE = "#5B8CFF"
BLUE_HOVER = "#4777E8"

GREEN = "#2DD4A4"
GREEN_HOVER = "#20B889"

RED = "#F87171"
AMBER = "#FBBF24"


# ---------------------------------------------------------------------------
# Image Explorer
# ---------------------------------------------------------------------------

class ImageExplorer(ctk.CTkToplevel):
    """Small in-app image browser with safe folder navigation."""

    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
    }

    def __init__(self, parent, initial_dir, on_select):
        super().__init__(parent)

        self.title("Open image")
        self.geometry("720x560")
        self.minsize(620, 440)
        self.configure(fg_color=APP_BG)

        self.transient(parent)
        self.grab_set()

        self.on_select = on_select

        self.current_dir = os.path.abspath(
            initial_dir
            if os.path.isdir(initial_dir)
            else os.getcwd()
        )

        self.history = []
        self.selected_path = None

        self._build_ui()
        self._show_directory(self.current_dir)

    # -----------------------------------------------------------------------
    # UI
    # -----------------------------------------------------------------------

    def _build_ui(self):
        header = ctk.CTkFrame(
            self,
            fg_color=SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
        )
        header.pack(
            fill="x",
            padx=18,
            pady=(18, 12),
        )

        ctk.CTkLabel(
            header,
            text="Open an image",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
            text_color=TEXT,
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 1),
        )

        ctk.CTkLabel(
            header,
            text="Browse folders or paste a folder path",
            font=ctk.CTkFont(size=12),
            text_color=MUTED,
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 13),
        )

        # Navigation
        navigation = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        navigation.pack(
            fill="x",
            padx=18,
        )

        self.back_button = ctk.CTkButton(
            navigation,
            text="‹",
            width=36,
            height=36,
            command=self._go_back,
            fg_color=SURFACE_ELEVATED,
            hover_color=BORDER,
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        )
        self.back_button.pack(
            side="left",
            padx=(0, 6),
        )

        ctk.CTkButton(
            navigation,
            text="↑",
            width=36,
            height=36,
            command=self._go_up,
            fg_color=SURFACE_ELEVATED,
            hover_color=BORDER,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        ).pack(
            side="left",
            padx=(0, 8),
        )

        self.path_entry = ctk.CTkEntry(
            navigation,
            height=36,
            fg_color=SURFACE,
            border_color=BORDER,
            text_color=TEXT,
        )
        self.path_entry.pack(
            side="left",
            fill="x",
            expand=True,
        )

        self.path_entry.bind(
            "<Return>",
            lambda _event: self._go_to_path(),
        )

        ctk.CTkButton(
            navigation,
            text="Go",
            width=54,
            height=36,
            command=self._go_to_path,
            fg_color=BLUE,
            hover_color=BLUE_HOVER,
        ).pack(
            side="left",
            padx=(8, 0),
        )

        # Location
        self.location_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            text_color=MUTED,
        )
        self.location_label.pack(
            fill="x",
            padx=23,
            pady=(13, 5),
        )

        # File list
        self.file_list = ctk.CTkScrollableFrame(
            self,
            fg_color=SURFACE,
            corner_radius=14,
            border_width=1,
            border_color=BORDER,
        )
        self.file_list.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=(0, 12),
        )

        # Bottom actions
        actions = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        actions.pack(
            fill="x",
            padx=18,
            pady=(0, 18),
        )

        self.selection_label = ctk.CTkLabel(
            actions,
            text="No image selected",
            text_color=MUTED,
            anchor="w",
            font=ctk.CTkFont(size=12),
        )
        self.selection_label.pack(
            side="left",
            fill="x",
            expand=True,
        )

        ctk.CTkButton(
            actions,
            text="Cancel",
            width=90,
            height=38,
            command=self.destroy,
            fg_color=SURFACE_ELEVATED,
            hover_color=BORDER,
        ).pack(
            side="right",
        )

        self.open_button = ctk.CTkButton(
            actions,
            text="Open image",
            width=110,
            height=38,
            command=self._open_selection,
            state="disabled",
            fg_color=GREEN,
            hover_color=GREEN_HOVER,
        )
        self.open_button.pack(
            side="right",
            padx=(0, 8),
        )

    # -----------------------------------------------------------------------
    # Directory handling
    # -----------------------------------------------------------------------

    def _show_directory(self, path, remember=True):
        path = os.path.abspath(path)

        if not os.path.isdir(path):
            self.location_label.configure(
                text="That folder does not exist",
                text_color=RED,
            )
            return

        if remember and path != self.current_dir:
            self.history.append(self.current_dir)

        self.current_dir = path
        self.selected_path = None

        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, path)

        self.location_label.configure(
            text="FOLDERS AND SUPPORTED IMAGES",
            text_color=MUTED,
        )

        self.selection_label.configure(
            text="No image selected",
            text_color=MUTED,
        )

        self.open_button.configure(
            state="disabled",
        )

        self.back_button.configure(
            state="normal" if self.history else "disabled",
        )

        for widget in self.file_list.winfo_children():
            widget.destroy()

        try:
            entries = sorted(
                os.scandir(path),
                key=lambda entry: (
                    not entry.is_dir(),
                    entry.name.lower(),
                ),
            )
        except OSError as error:
            self.location_label.configure(
                text=f"Cannot open folder: {error}",
                text_color=RED,
            )
            return

        visible = [
            entry
            for entry in entries
            if (
                entry.is_dir()
                or os.path.splitext(entry.name)[1].lower()
                in self.IMAGE_EXTENSIONS
            )
        ]

        if not visible:
            ctk.CTkLabel(
                self.file_list,
                text="No folders or supported images here.",
                text_color=MUTED,
            ).pack(
                pady=36,
            )
            return

        for entry in visible:
            is_folder = entry.is_dir()

            button = ctk.CTkButton(
                self.file_list,
                text=(
                    "Folder    "
                    if is_folder
                    else "Image     "
                ) + entry.name,
                anchor="w",
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color=SURFACE_ELEVATED,
                text_color=TEXT if is_folder else "#C9D6EA",
                command=lambda item=entry.path, folder=is_folder:
                    self._choose(item, folder),
            )

            button.pack(
                fill="x",
                padx=5,
                pady=2,
            )

    def _choose(self, path, is_folder):
        if is_folder:
            self._show_directory(path)
            return

        self.selected_path = path

        self.selection_label.configure(
            text=os.path.basename(path),
            text_color=TEXT,
        )

        self.open_button.configure(
            state="normal",
        )

    def _go_up(self):
        parent = os.path.dirname(self.current_dir)

        if parent != self.current_dir:
            self._show_directory(parent)

    def _go_back(self):
        if self.history:
            self._show_directory(
                self.history.pop(),
                remember=False,
            )

    def _go_to_path(self):
        path = os.path.expanduser(
            self.path_entry.get().strip()
        )

        self._show_directory(path)

    def _open_selection(self):
        if self.selected_path:
            self.on_select(self.selected_path)
            self.destroy()


# ---------------------------------------------------------------------------
# Main RoadDamageAI Application
# ---------------------------------------------------------------------------

class RoadDamageApp(ctk.CTk):
    """A focused two-panel viewer for road damage detection."""

    def __init__(self):
        super().__init__()

        self.title("RoadDamageAI")
        self.geometry("1180x800")
        self.minsize(960, 680)
        self.configure(fg_color=APP_BG)

        # -------------------------------------------------------------------
        # Paths
        # -------------------------------------------------------------------

        self.model_path = resource_path(
            os.path.join(
                "models",
                "best.pt",
            )
        )

        self.images_dir = resource_path(
            "test_images"
        )

        self.output_dir = resource_path(
            "output"
        )

        # -------------------------------------------------------------------
        # Model
        # -------------------------------------------------------------------

        self.model: YOLO | None = None

        # -------------------------------------------------------------------
        # Image state
        # -------------------------------------------------------------------

        self.current_image_path = None
        self.processed_image_cv = None
        self.current_detections = []

        self._image_sources = {
            "original": None,
            "result": None,
        }

        self._display_images = {
            "original": None,
            "result": None,
        }

        self._analysis_id = 0
        self._analysis_in_progress = False

        # -------------------------------------------------------------------
        # Damage classes
        # -------------------------------------------------------------------

        self.damage_names = {
            "D00": "Longitudinal crack",
            "D10": "Transverse crack",
            "D20": "Alligator crack",
            "D40": "Pothole",
            "D43": "Crosswalk blur",
            "D44": "White line blur",
            "D50": "Utility hole",
        }

        # -------------------------------------------------------------------
        # Start application
        # -------------------------------------------------------------------

        self._build_ui()
        self._load_model_async()

    # -----------------------------------------------------------------------
    # Main UI
    # -----------------------------------------------------------------------

    def _build_ui(self):
        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            1,
            weight=1,
        )

        # Header
        header = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=32,
            pady=(26, 18),
        )

        header.grid_columnconfigure(
            1,
            weight=1,
        )

        brand = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )

        brand.grid(
            row=0,
            column=0,
            sticky="w",
        )

        ctk.CTkLabel(
            brand,
            text="ROAD DAMAGE AI",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            text_color=BLUE,
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            brand,
            text="Inspection workspace",
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
            text_color=TEXT,
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        self.model_status = ctk.CTkLabel(
            header,
            text="  ●  Loading model  ",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            text_color=AMBER,
            fg_color="#332B16",
            corner_radius=14,
            height=30,
        )

        self.model_status.grid(
            row=0,
            column=2,
            sticky="e",
        )

        # Workspace
        workspace = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        workspace.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=32,
        )

        workspace.grid_columnconfigure(
            0,
            weight=3,
        )

        workspace.grid_columnconfigure(
            1,
            weight=2,
            minsize=300,
        )

        workspace.grid_rowconfigure(
            0,
            weight=1,
        )

        # Viewer
        viewer = ctk.CTkFrame(
            workspace,
            fg_color="transparent",
        )

        viewer.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 18),
        )

        viewer.grid_columnconfigure(
            (0, 1),
            weight=1,
        )

        viewer.grid_rowconfigure(
            1,
            weight=1,
        )

        self._section_label(
            viewer,
            "ORIGINAL",
            "Your selected road image",
            0,
        )

        self._section_label(
            viewer,
            "ANALYSIS",
            "Annotated detections",
            1,
        )

        self.original_card, self.original_view = self._image_card(
            viewer,
            0,
            "Choose an image to begin",
        )

        self.result_card, self.result_view = self._image_card(
            viewer,
            1,
            "Run analysis to see results",
        )

        # Sidebar
        sidebar = ctk.CTkFrame(
            workspace,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
        )

        sidebar.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        sidebar.grid_columnconfigure(
            0,
            weight=1,
        )

        ctk.CTkLabel(
            sidebar,
            text="Detection summary",
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
            text_color=TEXT,
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 3),
        )

        self.summary_label = ctk.CTkLabel(
            sidebar,
            text="Awaiting an image",
            font=ctk.CTkFont(size=12),
            text_color=MUTED,
        )

        self.summary_label.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20,
        )

        # Statistics
        stats = ctk.CTkFrame(
            sidebar,
            fg_color="transparent",
        )

        stats.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=18,
        )

        stats.grid_columnconfigure(
            (0, 1),
            weight=1,
        )

        self.count_value = self._stat_card(
            stats,
            "ISSUES",
            "—",
            0,
        )

        self.confidence_value = self._stat_card(
            stats,
            "TOP CONFIDENCE",
            "—",
            1,
        )

        divider = ctk.CTkFrame(
            sidebar,
            height=1,
            fg_color=BORDER,
        )

        divider.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
        )

        ctk.CTkLabel(
            sidebar,
            text="FOUND IN THIS IMAGE",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            text_color=MUTED,
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 8),
        )

        self.detection_list = ctk.CTkScrollableFrame(
            sidebar,
            fg_color="transparent",
            corner_radius=0,
        )

        self.detection_list.grid(
            row=5,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14),
        )

        sidebar.grid_rowconfigure(
            5,
            weight=1,
        )

        self._render_empty_results()

        # Actions
        actions = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        actions.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=32,
            pady=(18, 8),
        )

        actions.grid_columnconfigure(
            3,
            weight=1,
        )

        self.open_button = self._button(
            actions,
            "Open image",
            self.open_image,
            BLUE,
            BLUE_HOVER,
        )

        self.open_button.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.detect_button = self._button(
            actions,
            "Run analysis",
            self.start_detection_thread,
            GREEN,
            GREEN_HOVER,
        )

        self.detect_button.grid(
            row=0,
            column=1,
            padx=10,
            sticky="w",
        )

        self.save_button = self._button(
            actions,
            "Save result",
            self.save_result,
            SURFACE_ELEVATED,
            BORDER,
        )

        self.save_button.grid(
            row=0,
            column=2,
            sticky="w",
        )

        ctk.CTkButton(
            actions,
            text="Clear",
            command=self.clear_all,
            height=40,
            width=76,
            corner_radius=10,
            fg_color="transparent",
            hover_color=SURFACE,
            text_color=MUTED,
        ).grid(
            row=0,
            column=4,
            sticky="e",
        )

        # Footer
        footer = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )

        footer.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=32,
            pady=(0, 20),
        )

        self.status_label = ctk.CTkLabel(
            footer,
            text="Loading detection model…",
            anchor="w",
            font=ctk.CTkFont(size=12),
            text_color=MUTED,
        )

        self.status_label.pack(
            side="left",
        )

        self.progress = ctk.CTkProgressBar(
            footer,
            width=130,
            height=4,
            fg_color=SURFACE_ELEVATED,
            progress_color=BLUE,
        )

    # -----------------------------------------------------------------------
    # UI helper methods
    # -----------------------------------------------------------------------

    def _section_label(
        self,
        parent,
        title,
        subtitle,
        column,
    ):
        label = ctk.CTkFrame(
            parent,
            fg_color="transparent",
        )

        label.grid(
            row=0,
            column=column,
            sticky="w",
            pady=(0, 8),
            padx=(0, 8) if column == 0 else (8, 0),
        )

        ctk.CTkLabel(
            label,
            text=title,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            text_color=MUTED,
        ).pack(
            anchor="w",
        )

        ctk.CTkLabel(
            label,
            text=subtitle,
            font=ctk.CTkFont(size=13),
            text_color=TEXT,
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

    def _image_card(
        self,
        parent,
        column,
        placeholder,
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER,
        )

        card.grid(
            row=1,
            column=column,
            sticky="nsew",
            padx=(0, 8) if column == 0 else (8, 0),
        )

        card.grid_columnconfigure(
            0,
            weight=1,
        )

        card.grid_rowconfigure(
            0,
            weight=1,
        )

        view = ctk.CTkLabel(
            card,
            text=placeholder,
            font=ctk.CTkFont(size=14),
            text_color=MUTED,
        )

        view.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=18,
            pady=18,
        )

        return card, view

    def _stat_card(
        self,
        parent,
        title,
        value,
        column,
    ):
        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE_ELEVATED,
            corner_radius=12,
        )

        card.grid(
            row=0,
            column=column,
            sticky="ew",
            padx=(0, 5) if column == 0 else (5, 0),
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                size=9,
                weight="bold",
            ),
            text_color=MUTED,
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 0),
        )

        label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
            text_color=TEXT,
        )

        label.pack(
            anchor="w",
            padx=12,
            pady=(2, 10),
        )

        return label

    @staticmethod
    def _button(
        parent,
        text,
        command,
        color,
        hover,
    ):
        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=40,
            corner_radius=10,
            fg_color=color,
            hover_color=hover,
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )

    # -----------------------------------------------------------------------
    # Model loading
    # -----------------------------------------------------------------------

    def _load_model_async(self):
        def load():
            try:
                if not os.path.isfile(self.model_path):
                    raise FileNotFoundError(
                        f"Model file not found: {self.model_path}"
                    )

                self.model = YOLO(
                    self.model_path
                )

                self.after(
                    0,
                    lambda: self._set_model_status(
                        "  ●  Model ready  ",
                        GREEN,
                        "#12352D",
                    ),
                )

                self.after(
                    0,
                    self._on_model_ready,
                )

            except Exception as error:
                self.after(
                    0,
                    lambda: self._set_model_status(
                        "  ●  Model unavailable  ",
                        RED,
                        "#3B1D29",
                    ),
                )

                self.after(
                    0,
                    lambda: self._set_status(
                        f"Could not load model: {error}",
                        RED,
                    ),
                )

        threading.Thread(
            target=load,
            daemon=True,
        ).start()

    # -----------------------------------------------------------------------
    # Image handling
    # -----------------------------------------------------------------------

    def open_image(self):
        ImageExplorer(
            self,
            self.images_dir,
            self._load_image,
        )

    def _load_image(self, path):
        self.current_image_path = path
        self.processed_image_cv = None
        self.current_detections = []

        self._analysis_id += 1

        self._set_image(
            "original",
            path,
        )

        self._clear_image(
            "result",
            "Analyzing image…",
        )

        self._render_empty_results(
            "Preparing analysis"
        )

        if self.model:
            self.start_detection_thread()
        else:
            self._set_status(
                f"Loaded {os.path.basename(path)} — "
                "waiting for the model to finish loading.",
                AMBER,
            )

    # -----------------------------------------------------------------------
    # Detection
    # -----------------------------------------------------------------------

    def start_detection_thread(self):
        if not self.current_image_path:
            self._set_status(
                "Choose an image before running analysis.",
                RED,
            )
            return

        if self.model is None:
            self._set_status(
                "The model is still loading. Please wait a moment.",
                AMBER,
            )
            return

        if self._analysis_in_progress:
            self._set_status(
                "New image queued — analysis will start shortly.",
                AMBER,
            )
            return

        image_path = self.current_image_path
        analysis_id = self._analysis_id

        self._analysis_in_progress = True

        self.detect_button.configure(
            state="disabled",
            text="Analyzing…",
        )

        self.progress.pack(
            side="right",
            pady=8,
        )

        self.progress.configure(
            mode="indeterminate",
        )

        self.progress.start()

        self._set_status(
            "Analyzing road surface…",
            BLUE,
        )

        threading.Thread(
            target=self._run_detection,
            args=(image_path, analysis_id),
            daemon=True,
        ).start()

    def _run_detection(
        self,
        image_path,
        analysis_id,
    ):
        try:
            # ---------------------------------------------------------------
            # Keep a local reference.
            # This fixes Pylance's warning that self.model might be None.
            # ---------------------------------------------------------------

            model = self.model

            if model is None:
                raise RuntimeError(
                    "YOLO model is not loaded"
                )

            # ---------------------------------------------------------------
            # YOLO inference
            # ---------------------------------------------------------------

            results = model.predict(
                source=image_path,
                conf=0.35,
                iou=0.45,
                save=False,
                verbose=False,
            )

            # ---------------------------------------------------------------
            # Read image using OpenCV
            # ---------------------------------------------------------------

            image = cv2.imread(
                image_path
            )

            if image is None:
                raise ValueError(
                    "image could not be read"
                )

            items = []

            # ---------------------------------------------------------------
            # Process detections
            # ---------------------------------------------------------------

            for box in results[0].boxes:
                class_id = model.names[
                    int(box.cls[0])
                ]

                confidence = float(
                    box.conf[0]
                )

                damage = self.damage_names.get(
                    class_id,
                    class_id,
                )

                items.append(
                    (
                        damage,
                        confidence * 100,
                    )
                )

                # Bounding box coordinates
                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0],
                )

                # Draw bounding box
                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (73, 226, 172),
                    2,
                )

                # Detection label
                label = (
                    f"{damage}  "
                    f"{confidence:.0%}"
                )

                cv2.putText(
                    image,
                    label,
                    (
                        x1,
                        max(y1 - 8, 20),
                    ),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (73, 226, 172),
                    2,
                    cv2.LINE_AA,
                )

            # ---------------------------------------------------------------
            # Send result back to GUI thread
            # ---------------------------------------------------------------

            self.after(
                0,
                lambda: self._finish_detection(
                    image,
                    items,
                    analysis_id,
                ),
            )

        except Exception as error:
            self.after(
                0,
                lambda: self._detection_error(
                    str(error),
                    analysis_id,
                ),
            )

    # -----------------------------------------------------------------------
    # Detection results
    # -----------------------------------------------------------------------

    def _finish_detection(
        self,
        image,
        items,
        analysis_id,
    ):
        # Ignore an old detection if a newer image was selected.
        if analysis_id != self._analysis_id:
            self._stop_progress()

            if self.current_image_path:
                self.start_detection_thread()

            return

        self._stop_progress()

        self.processed_image_cv = image
        self.current_detections = items

        self._set_image(
            "result",
            image,
            cv_image=True,
        )

        self._render_results(
            items
        )

        self._set_status(
            f"Analysis complete — "
            f"{len(items)} issue"
            f"{'s' if len(items) != 1 else ''} found.",
            GREEN,
        )

    def _detection_error(
        self,
        message,
        analysis_id,
    ):
        if analysis_id != self._analysis_id:
            self._stop_progress()

            if self.current_image_path:
                self.start_detection_thread()

            return

        self._stop_progress()

        self._set_status(
            f"Analysis failed: {message}",
            RED,
        )

    def _stop_progress(self):
        self.progress.stop()
        self.progress.pack_forget()

        self._analysis_in_progress = False

        self.detect_button.configure(
            state="normal",
            text="Run analysis",
        )

    # -----------------------------------------------------------------------
    # Save result
    # -----------------------------------------------------------------------

    def save_result(self):
        if self.processed_image_cv is None:
            self._set_status(
                "Run analysis before saving a result.",
                RED,
            )
            return

        os.makedirs(
            self.output_dir,
            exist_ok=True,
        )

        name = os.path.splitext(
            os.path.basename(
                self.current_image_path
            )
        )[0]

        path = os.path.join(
            self.output_dir,
            f"detected_{name}.png",
        )

        if cv2.imwrite(
            path,
            self.processed_image_cv,
        ):
            self._set_status(
                f"Saved result to "
                f"output/{os.path.basename(path)}",
                GREEN,
            )
        else:
            self._set_status(
                "Could not save the result image.",
                RED,
            )

    # -----------------------------------------------------------------------
    # Clear workspace
    # -----------------------------------------------------------------------

    def clear_all(self):
        self._analysis_id += 1

        self.current_image_path = None
        self.processed_image_cv = None
        self.current_detections = []

        self._clear_image(
            "original",
            "Choose an image to begin",
        )

        self._clear_image(
            "result",
            "Run analysis to see results",
        )

        self._render_empty_results()

        self._set_status(
            "Workspace cleared",
            MUTED,
        )

    # -----------------------------------------------------------------------
    # Model ready
    # -----------------------------------------------------------------------

    def _on_model_ready(self):
        if self.current_image_path:
            self._set_status(
                "Model ready — starting analysis…",
                BLUE,
            )

            self.start_detection_thread()
        else:
            self._set_status(
                "Model is ready. "
                "Choose a road image to begin.",
                MUTED,
            )

    # -----------------------------------------------------------------------
    # Display images
    # -----------------------------------------------------------------------

    def _set_image(
        self,
        target,
        source,
        cv_image=False,
    ):
        if target == "original":
            card = self.original_card
            label = self.original_view
        else:
            card = self.result_card
            label = self.result_view

        try:
            if cv_image:
                image = Image.fromarray(
                    cv2.cvtColor(
                        source,
                        cv2.COLOR_BGR2RGB,
                    )
                )
            else:
                image = Image.open(
                    source
                )

            image = ImageOps.exif_transpose(
                image
            ).convert("RGB")

            width = max(
                card.winfo_width() - 36,
                260,
            )

            height = max(
                card.winfo_height() - 36,
                260,
            )

            image.thumbnail(
                (width, height),
                Image.Resampling.LANCZOS,
            )

            visual = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size,
            )

            # Clear the native Tk image first.
            label._label.configure(
                image=""
            )

            label.configure(
                image=visual
            )

            label.configure(
                text=""
            )

            self._display_images[target] = visual
            self._image_sources[target] = source

        except Exception as error:
            self._clear_image(
                target,
                f"Unable to display image\n{error}",
            )

    def _clear_image(
        self,
        target,
        text,
    ):
        if target == "original":
            label = self.original_view
        else:
            label = self.result_view

        # Clear native Tk image.
        label._label.configure(
            image=""
        )

        label.configure(
            image=None
        )

        label.configure(
            text=text
        )

        self._display_images[target] = None
        self._image_sources[target] = None

    # -----------------------------------------------------------------------
    # Detection result list
    # -----------------------------------------------------------------------

    def _render_results(self, items):
        for widget in self.detection_list.winfo_children():
            widget.destroy()

        self.count_value.configure(
            text=str(len(items))
        )

        self.confidence_value.configure(
            text=(
                f"{max(score for _, score in items):.0f}%"
                if items
                else "—"
            )
        )

        if not items:
            self.summary_label.configure(
                text="No visible road damage detected"
            )

            self._render_empty_results(
                "No detections above the confidence threshold"
            )

            return

        types = Counter(
            name
            for name, _ in items
        )

        self.summary_label.configure(
            text=(
                f"{len(items)} detection"
                f"{'s' if len(items) != 1 else ''} "
                f"across {len(types)} type"
                f"{'s' if len(types) != 1 else ''}"
            )
        )

        for name, score in sorted(
            items,
            key=lambda item: item[1],
            reverse=True,
        ):
            row = ctk.CTkFrame(
                self.detection_list,
                fg_color=SURFACE_ELEVATED,
                corner_radius=10,
            )

            row.pack(
                fill="x",
                pady=4,
                padx=2,
            )

            ctk.CTkLabel(
                row,
                text=name,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
                text_color=TEXT,
            ).pack(
                side="left",
                padx=11,
                pady=10,
            )

            ctk.CTkLabel(
                row,
                text=f"{score:.0f}%",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
                text_color=GREEN,
            ).pack(
                side="right",
                padx=11,
            )

    def _render_empty_results(
        self,
        text="No detections yet",
    ):
        for widget in self.detection_list.winfo_children():
            widget.destroy()

        self.count_value.configure(
            text="—"
        )

        self.confidence_value.configure(
            text="—"
        )

        self.summary_label.configure(
            text=(
                "Awaiting an image"
                if text == "No detections yet"
                else text
            )
        )

        ctk.CTkLabel(
            self.detection_list,
            text=text,
            wraplength=240,
            justify="left",
            text_color=MUTED,
            font=ctk.CTkFont(size=12),
        ).pack(
            anchor="w",
            padx=8,
            pady=12,
        )

    # -----------------------------------------------------------------------
    # Status helpers
    # -----------------------------------------------------------------------

    def _set_model_status(
        self,
        text,
        color,
        background,
    ):
        self.model_status.configure(
            text=text,
            text_color=color,
            fg_color=background,
        )

    def _set_status(
        self,
        text,
        color=MUTED,
    ):
        self.status_label.configure(
            text=text,
            text_color=color,
        )


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = RoadDamageApp()
    app.mainloop()