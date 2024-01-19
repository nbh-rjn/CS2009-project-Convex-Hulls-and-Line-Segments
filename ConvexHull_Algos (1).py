import tkinter as tk
import math
import time

class ConvexHullApp:
    def __init__(self, master, width, height):
        self.master = master
        self.master.title("Convex Hull Algorithms")
        self.canvas = tk.Canvas(master, width=width, height=height, bg="black")
        self.canvas.pack()

        self.points = []
        self.convex_hull = []
        self.start_time = 0

        self.canvas.bind("<Button-1>", self.add_point)

        # Algorithm selection dropdown menu
        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("Graham Scan")  # Default selection
        algorithms = ["Graham Scan", "Brute Force", "Jarvis March", "Andrew's Monotone Chain", "Quick Hull"]
        self.algorithm_menu = tk.OptionMenu(master, self.algorithm_var, *algorithms)
        self.algorithm_menu.pack()

        self.draw_button = tk.Button(master, text="Draw Convex Hull", command=self.draw_convex_hull)
        self.draw_button.pack()

        self.time_label = tk.Label(master, text="Time Elapsed: 0 seconds")
        self.time_label.pack()

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_canvas)
        self.reset_button.pack()

        # Draw x and y axes with a small gap
        gap = 10
        self.canvas.create_line(gap, height - gap, width, height - gap, fill="black", width=2)  # x-axis
        self.canvas.create_line(gap, gap, gap, height - gap, fill="black", width=2)  # y-axis
        self.canvas.create_text(width - 20, height - gap + 20, text="X", anchor="w", fill="black",
                                font=("Helvetica", 12, "bold"))
        self.canvas.create_text(gap + 20, gap + 20, text="Y", anchor="w", fill="black", font=("Helvetica", 12, "bold"))

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")
        self.canvas.create_text(x + 10, y - 10, text=f"({x}, {y})", anchor="w", fill="blue")

    def draw_convex_hull(self):
        if len(self.points) < 3:
            return

        # Delete the previous convex hull
        self.canvas.delete("convex_hull")

        self.start_time = time.time()  # Record the start time
        algorithm = self.algorithm_var.get()

        if algorithm == "Graham Scan":
            self.convex_hull = self.graham_scan()
        elif algorithm == "Brute Force":
            self.convex_hull = self.brute_force_convex_hull()
        elif algorithm == "Jarvis March":
            self.convex_hull = self.jarvis_march_convex_hull()
            # Draw the convex hull with delays
            for i in range(len(self.convex_hull) - 1):
                self.draw_line_segment(self.convex_hull[i], self.convex_hull[i + 1], color="orange")
                time.sleep(0.5)  # Adjust the delay (in seconds) between each line segment
                self.master.update()
            # Draw the last line segment to close the convex hull
            self.draw_line_segment(self.convex_hull[-1], self.convex_hull[0], color="orange")
            time.sleep(0.5)  # Adjust the delay (in seconds) for the final line segment
            self.master.update()
        elif algorithm == "Andrew's Monotone Chain":
            self.convex_hull = self.andrew_monotone_chain()

            # Draw the convex hull with delays
            for i in range(len(self.convex_hull) - 1):
                self.draw_line_segment(self.convex_hull[i], self.convex_hull[i + 1], color="green")
                time.sleep(0.5)  # Adjust the delay (in seconds) between each line segment
                self.master.update()

            # Draw the last line segment to close the convex hull
            self.draw_line_segment(self.convex_hull[-1], self.convex_hull[0], color="green")
            time.sleep(0.5)  # Adjust the delay (in seconds) for the final line segment
            self.master.update()
        elif algorithm == "Quick Hull":
            self.convex_hull = self.quick_hull_convex_hull()
            # Draw the convex hull with delays
            for i in range(len(self.convex_hull)):
                next_index = (i + 1) % len(self.convex_hull)
                self.draw_line_segment(self.convex_hull[i], self.convex_hull[next_index], color="purple")
                time.sleep(0.5)  # Adjust the delay (in seconds) between each line segment
                self.master.update()
            # Draw the last line segment to close the convex hull
            self.draw_line_segment(self.convex_hull[-1], self.convex_hull[0], color="purple")
            time.sleep(0.5)  # Adjust the delay (in seconds) for the final line segment
            self.master.update()

        elapsed_time = time.time() - self.start_time
        self.update_time_label(elapsed_time)

        # Draw the convex hull
        if self.convex_hull:
            self.canvas.create_polygon(self.convex_hull, outline="blue", fill="", width=2, tags="convex_hull")

    def reset_canvas(self):
        # Reset canvas by deleting all points and the convex hull
        self.canvas.delete("all")
        self.points = []
        self.convex_hull = []
        self.start_time = 0
        self.update_time_label(0)

        # Redraw x and y axes with a small gap
        gap = 10
        self.canvas.create_line(gap, self.canvas.winfo_reqheight() - gap, self.canvas.winfo_reqwidth(),
                                self.canvas.winfo_reqheight() - gap, fill="black", width=2)  # x-axis
        self.canvas.create_line(gap, gap, gap, self.canvas.winfo_reqheight() - gap, fill="black", width=2)  # y-axis
        self.canvas.create_text(self.canvas.winfo_reqwidth() - 20, self.canvas.winfo_reqheight() - gap + 20, text="X",
                                anchor="w", fill="black",
                                font=("Helvetica", 12, "bold"))
        self.canvas.create_text(gap + 20, gap + 20, text="Y", anchor="w", fill="black", font=("Helvetica", 12, "bold"))

    def graham_scan(self):
        def polar_angle(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return math.atan2(y2 - y1, x2 - x1)

        def orientation(p1, p2, p3):
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = p3
            val = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)
            if val == 0:
                return 0  # Collinear
            return 1 if val > 0 else -1  # Clockwise or Counterclockwise

        reference_point = min(self.points, key=lambda p: (p[1], p[0]))
        sorted_points = [reference_point] + sorted(self.points[1:],
                                                   key=lambda p: (
                                                       polar_angle(reference_point, p), p[0] - reference_point[0],
                                                       p[1] - reference_point[1]),
                                                   reverse=True)

        # Label all sorted points
        for i, point in enumerate(sorted_points):
            x, y = point
            label = f"p{i}"
            self.canvas.create_text(x - 10, y - 10, text=label, anchor="w", fill="blue")

        # Initialize the convex hull with the first three sorted points
        convex_hull = [sorted_points[0], sorted_points[1]]
        self.draw_line_segment(convex_hull[-1], convex_hull[-2])
        convex_hull.append(sorted_points[2])
        self.draw_line_segment(convex_hull[-1], convex_hull[-2])

        # Iterate through the remaining sorted points
        for i in range(3, len(sorted_points)):
            while len(convex_hull) > 1 and orientation(convex_hull[-2], convex_hull[-1], sorted_points[i]) != 1:
                # Pop points until a left turn is encountered
                last_point = convex_hull.pop()
                self.draw_line_segment(last_point, convex_hull[-1], color="white")

            # Push the current point onto the stack
            convex_hull.append(sorted_points[i])
            self.draw_line_segment(convex_hull[-2], sorted_points[i])

        # Draw the last line segment to close the convex hull
        self.draw_line_segment(convex_hull[-1], convex_hull[0])

        return convex_hull

    def brute_force_convex_hull(self):
        def is_inside_triangle(p1, p2, p3, test_point):
            def orientation(a, b, c):
                val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
                if val == 0:
                    return 0  # Collinear
                return 1 if val > 0 else -1  # Clockwise or Counterclockwise

            o1 = orientation(p1, p2, test_point)
            o2 = orientation(p2, p3, test_point)
            o3 = orientation(p3, p1, test_point)

            return o1 == o2 == o3

        n = len(self.points)
        convex_hull = []

        if n < 3:
            return convex_hull  # Convex hull is not possible with less than 3 points

        # Clear previous convex hulls
        self.canvas.delete("convex_hull")

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    is_convex_hull = True
                    for point in self.points:
                        if point != self.points[i] and point != self.points[j] and point != self.points[k]:
                            if is_inside_triangle(self.points[i], self.points[j], self.points[k], point):
                                is_convex_hull = False
                                break

                    if is_convex_hull:
                        convex_hull.append(self.points[i])
                        convex_hull.append(self.points[j])
                        convex_hull.append(self.points[k])

                        # Draw the triangle
                        self.draw_line_segment(self.points[i], self.points[j])
                        self.draw_line_segment(self.points[j], self.points[k])
                        self.draw_line_segment(self.points[k], self.points[i])

        return convex_hull

    def draw_line_segment(self, p1, p2, color="red"):
        x1, y1 = p1
        x2, y2 = p2
        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, tags="convex_hull")
        self.master.update()
        self.master.after(500)  # Adjust the delay (in milliseconds) between each line segment

    def update_time_label(self, elapsed_time):
        self.time_label.config(text=f"Time Elapsed: {elapsed_time:.2f} seconds")

    def jarvis_march_convex_hull(self):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        def next_point(p, q):
            next_pt = 0
            for i in range(len(self.points)):
                if orientation(p, self.points[i], q) == 2:
                    next_pt = i
                    q = self.points[i]
            return next_pt

        hull = []

        # Find the point with the lowest y-coordinate (and leftmost if ties)
        start_point = min(self.points, key=lambda p: (p[1], p[0]))

        p = start_point
        q = None

        while q != start_point:
            hull.append(p)
            q = self.points[0]
            for r in self.points[1:]:
                if q == p or orientation(p, q, r) == 2:
                    q = r

            p = q

        return hull

    def andrew_monotone_chain(self):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            return 1 if val > 0 else 2

        # Sort points lexicographically
        sorted_points = sorted(self.points)

        # Lower hull
        lower_hull = []
        for p in sorted_points:
            while len(lower_hull) >= 2 and orientation(lower_hull[-2], lower_hull[-1], p) != 2:
                lower_hull.pop()
            lower_hull.append(p)

        # Upper hull
        upper_hull = []
        for p in reversed(sorted_points):
            while len(upper_hull) >= 2 and orientation(upper_hull[-2], upper_hull[-1], p) != 2:
                upper_hull.pop()
            upper_hull.append(p)

        # Combine the lower and upper hulls to form the convex hull
        convex_hull = lower_hull[:-1] + upper_hull[:-1]

        return convex_hull

    def quick_hull_convex_hull(self):
        def find_side(p1, p2, p):
            val = (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])
            if val > 0:
                return 1
            if val < 0:
                return -1
            return 0

        def line_dist(p1, p2, p):
            return abs((p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0]))

        def quick_hull_recursive(a, n, p1, p2, side, convex_hull):
            ind = -1
            max_dist = 0
            for i in range(n):
                temp = line_dist(p1, p2, a[i])

                if (find_side(p1, p2, a[i]) == side) and (temp > max_dist):
                    ind = i
                    max_dist = temp

            if ind == -1:
                convex_hull.append(tuple(p1))
                convex_hull.append(tuple(p2))
                return

            quick_hull_recursive(a, n, a[ind], p1, -find_side(a[ind], p1, p2), convex_hull)
            quick_hull_recursive(a, n, a[ind], p2, -find_side(a[ind], p2, p1), convex_hull)

        n = len(self.points)
        convex_hull = []

        if n < 3:
            return convex_hull  # Convex hull is not possible with less than 3 points

        min_x = 0
        max_x = 0
        for i in range(1, n):
            if self.points[i][0] < self.points[min_x][0]:
                min_x = i
            if self.points[i][0] > self.points[max_x][0]:
                max_x = i

        quick_hull_recursive(self.points, n, self.points[min_x], self.points[max_x], 1, convex_hull)
        quick_hull_recursive(self.points, n, self.points[min_x], self.points[max_x], -1, convex_hull)

        return convex_hull

def main():
    root = tk.Tk()
    app = ConvexHullApp(root, width=900, height=600)
    root.mainloop()

if __name__ == "__main__":
    main()
