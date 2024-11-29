import tkinter as tk

def orientation_ccw(p1, p2, p3):
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else -1  # Counter-clockwise or Clockwise

def orientation(param_p, param_q, param_r):
    cross_product = (param_q[0] - param_p[0]) * (param_r[1] - param_p[1]) - (param_q[1] - param_p[1]) * (param_r[0] - param_p[0])
    if cross_product == 0:
        return 0  # Collinear
    return 1 if cross_product > 0 else -1  # Counter-clockwise or Clockwise

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def do_segments_intersect_ccw(p1, q1, p2, q2):
    o1 = orientation_ccw(p1, q1, p2)
    o2 = orientation_ccw(p1, q1, q2)
    o3 = orientation_ccw(p2, q2, p1)
    o4 = orientation_ccw(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True  # General case, line segments intersect

    if o1 == 0 and on_segment(p1, p2, q1):
        return True  # p1, q1, p2 are collinear and p2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True  # p1, q1, q2 are collinear and q2 lies on segment p1q1
    if o3 == 0 and on_segment(p2, p1, q2):
        return True  # p2, q2, p1 are collinear and p1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True  # p2, q2, q1 are collinear and q1 lies on segment p2q2

    return False  # Doesn't fall into any of the above cases

def do_segments_intersect_franklin_ant(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True  # General case, line segments intersect

    if o1 == 0 and on_segment(p1, p2, q1):
        return True  # p1, q1, p2 are collinear and p2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True  # p1, q1, q2 are collinear and q2 lies on segment p1q1
    if o3 == 0 and on_segment(p2, p1, q2):
        return True  # p2, q2, p1 are collinear and p1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True  # p2, q2, q1 are collinear and q1 lies on segment p2q2

    return False  # Doesn't fall into any of the above cases

def parametric_equation(t, p1, p2):
    x = p1[0] + t * (p2[0] - p1[0])
    y = p1[1] + t * (p2[1] - p1[1])
    return x, y

def do_segments_intersect_parametric(p1, q1, p2, q2):
    t_numer = (q2[0] - p2[0]) * (p1[1] - p2[1]) - (q2[1] - p2[1]) * (p1[0] - p2[0])
    t_denom = (q2[1] - p2[1]) * (q1[0] - p1[0]) - (q2[0] - p2[0]) * (q1[1] - p1[1])
    if t_denom == 0:
        return False  # Lines are parallel
    t = t_numer / t_denom
    if 0 <= t <= 1:
        intersection_point = parametric_equation(t, p1, q1)
        return True, intersection_point
    else:
        return False

class LineIntersectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Line Intersection Checker")

        self.canvas = tk.Canvas(root, width=900, height=600, bg="black")
        self.canvas.pack()

        self.points = []

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_canvas)
        self.reset_button.pack()

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("CCW")  # Default algorithm
        self.algorithm_menu = tk.OptionMenu(root, self.algorithm_var, "CCW", "Franklin Antonio", "Parametric")
        self.algorithm_menu.pack()

        self.intersect_label = tk.Label(root, text="", fg="green", font="Helvetica 12 bold")
        self.intersect_label.pack()

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")

        if len(self.points) == 4:
            algorithm_choice = self.algorithm_var.get()
            if algorithm_choice == "CCW":
                result = do_segments_intersect_ccw(self.points[0], self.points[1], self.points[2], self.points[3])
            elif algorithm_choice == "Franklin Antonio":
                result = do_segments_intersect_franklin_ant(self.points[0], self.points[1], self.points[2], self.points[3])
            elif algorithm_choice == "Parametric":
                result = do_segments_intersect_parametric(self.points[0], self.points[1], self.points[2], self.points[3])

            print(f"Segments {'intersect' if result else 'do not intersect'}.")

            if result:
                self.draw_line(self.points[0], self.points[1], "blue")
                self.draw_line(self.points[2], self.points[3], "blue")
                if algorithm_choice == "Parametric":
                    intersection_result, intersection_point = result
                    if intersection_result:
                        self.canvas.create_oval(intersection_point[0] - 3, intersection_point[1] - 3,
                                                intersection_point[0] + 3, intersection_point[1] + 3, fill="green")
            else:
                self.draw_line(self.points[0], self.points[1], "red")
                self.draw_line(self.points[2], self.points[3], "red")

            self.intersect_label.config(text="Segments Intersect" if result else "Segments Do Not Intersect", fg="green" if result else "red")

    def draw_line(self, p1, p2, color):
        self.canvas.create_line(p1, p2, fill=color)

    def reset_canvas(self):
        self.points = []
        self.canvas.delete("all")
        self.intersect_label.config(text="", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = LineIntersectionApp(root)
    root.mainloop()
