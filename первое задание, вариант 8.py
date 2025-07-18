import math
import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
class FunctionPlotter:
    def __init__(self):
        self.A = 9.66459
        self.x_min, self.x_max = -10, 10
        self.step = 0.1
        self.x_values, self.y_values = self.calculate_function()
        self.save_to_xml_exact_format()
        self.plot_graph()
    def calculate_function(self):
        x_values = []
        current = self.x_min
        while current <= self.x_max + self.step/2:
            x_values.append(round(current, 2))
            current += self.step
        y_values = []
        for x in x_values:
            try:
                exponent = 1 - math.sqrt(x**2 + self.A**2)/math.pi
                y = -math.sin(x) * math.cos(self.A) * math.exp(exponent)
                y_values.append(round(y, 6))
            except:
                y_values.append(float('nan'))
        return x_values, y_values
    def save_to_xml_exact_format(self):
        xml_declaration = '<?xml version="1.1" encoding="UTF-8"?>'
        root = ET.Element("data")
        xdata = ET.SubElement(root, "xdata")
        ydata = ET.SubElement(root, "ydata")
        for x in self.x_values:
            x_elem = ET.SubElement(xdata, "x")
            x_elem.text = str(x)
        for y in self.y_values:
            y_elem = ET.SubElement(ydata, "y")
            y_elem.text = str(y)
        xml_str = xml_declaration + "\n"
        xml_str += ET.tostring(root, encoding='unicode')
        xml_str = xml_str.replace("><", ">\n<")
        with open("result.xml", "w", encoding="utf-8") as f:
            f.write(xml_str)
        messagebox.showinfo("Готово", "Файл result.xml создан")
    def plot_graph(self):
        root = tk.Tk()
        root.title(f"График функции (вариант 8)")
        canvas = tk.Canvas(root, width=800, height=600, bg="white")
        canvas.pack(pady=10)
        width, height = 800, 600
        padding = 50
        valid_points = [(x, y) for x, y in zip(self.x_values, self.y_values) 
                       if not math.isnan(y)]
        if not valid_points:
            return
        x_vals, y_vals = zip(*valid_points)
        x_min, x_max = min(x_vals), max(x_vals)
        y_min, y_max = min(y_vals), max(y_vals)
        def scale_x(x):
            return padding + (x - x_min)/(x_max - x_min) * (width - 2*padding)
        def scale_y(y):
            return height - padding - (y - y_min)/(y_max - y_min) * (height - 2*padding)
        grid_color = "#e0e0e0"
        for x in range(int(x_min), int(x_max)+1):
            x_pos = scale_x(x)
            canvas.create_line(x_pos, padding, x_pos, height-padding, 
                             fill=grid_color, dash=(2,2))
        y_step = self.calculate_optimal_step(y_max - y_min)
        y = math.ceil(y_min/y_step)*y_step
        while y <= y_max:
            y_pos = scale_y(y)
            canvas.create_line(padding, y_pos, width-padding, y_pos, 
                             fill=grid_color, dash=(2,2))
            y += y_step
        canvas.create_line(padding, scale_y(0), width-padding, scale_y(0), width=2)
        canvas.create_line(scale_x(0), padding, scale_x(0), height-padding, width=2)
        canvas.create_text(width//2, scale_y(0)-20, text="x", font=("Arial", 12))
        canvas.create_text(scale_x(0)+20, padding//2, text="y", font=("Arial", 12))
        for x in range(int(x_min), int(x_max)+1):
            if x != 0:
                x_pos = scale_x(x)
                canvas.create_line(x_pos, scale_y(0)-5, x_pos, scale_y(0)+5, width=2)
                canvas.create_text(x_pos, scale_y(0)+20, text=str(x), font=("Arial", 10))
        y = math.ceil(y_min/y_step)*y_step
        while y <= y_max:
            y_pos = scale_y(y)
            if abs(y) > 0.01*y_step:
                canvas.create_line(scale_x(0)-5, y_pos, scale_x(0)+5, y_pos, width=2)
                canvas.create_text(scale_x(0)-20, y_pos, text=f"{y:.2f}", 
                                 font=("Arial", 10), anchor="e")
            y += y_step
        points = [(scale_x(x), scale_y(y)) for x, y in valid_points]
        for i in range(len(points)-1):
            canvas.create_line(points[i][0], points[i][1], 
                             points[i+1][0], points[i+1][1], 
                             fill="blue", width=2)
        info_text = f"Файл: result.xml (сохранен по заданному шаблону)\n" \
                   f"Точек: {len(valid_points)} | x ∈ [{self.x_min}, {self.x_max}] | шаг: {self.step}"
        tk.Label(root, text=info_text).pack()
        root.mainloop()
    def calculate_optimal_step(self, y_range):
        step = 10**math.floor(math.log10(y_range))
        if y_range/step > 10:
            step /= 2
        elif y_range/step < 4:
            step /= 5
        return step
if __name__ == "__main__":
    FunctionPlotter()
