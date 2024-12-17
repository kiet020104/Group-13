from turtle import Turtle, Screen
import random
import time

# Màu sắc cho các phương tiện giao thông
COLORS = ["red", "green", "blue", "yellow", "cyan", "purple"]

# Quản lý bảng điểm cao
class HighScoreManager:
    def __init__(self, file_name="scores.txt"):
        # Hàm khởi tạo, nhận tên file để lưu trữ điểm cao
        self.file_name = file_name
        self.scores = self.load_scores()  # Tải bảng điểm từ file vào

    def load_scores(self):
        try:
            with open(self.file_name, "r") as file:
                # Đọc tất cả các dòng từ file và tách tên và điểm số
                scores = [line.strip().split(": ") for line in file.readlines()]
                # Sắp xếp bảng điểm theo điểm số (giảm dần)
                return sorted(scores, key=lambda x: int(x[1]), reverse=True)
        except FileNotFoundError:
            # Nếu không tìm thấy file, trả về bảng điểm rỗng
            return []

    def save_score(self, name, score):
        found = False
        # Kiểm tra xem người chơi đã có trong bảng điểm chưa
        for idx, (player, current_score) in enumerate(self.scores):
            if player == name:
                # Nếu điểm mới cao hơn điểm cũ, cập nhật điểm
                if int(current_score) < score:
                    self.scores[idx] = (name, str(score))
                found = True
                break
        
        if not found:
            # Nếu chưa có tên người chơi, thêm mới vào bảng điểm
            self.scores.append((name, str(score)))
        
        # Sắp xếp lại bảng điểm theo điểm số
        self.scores = sorted(self.scores, key=lambda x: int(x[1]), reverse=True)
        
        # Lưu bảng điểm vào file
        with open(self.file_name, "w") as file:
            for player, score in self.scores:
                file.write(f"{player}: {score}\n")

    def display_high_scores(self):
        # Hiển thị 5 điểm cao nhất
        print("\nHigh Scores:")
        for idx, (player, score) in enumerate(self.scores[:5], start=1):
            print(f"{idx}. {player}: {score}")

# Lớp đại diện cho nhân vật chính - rùa
class TurtleCross(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("turtle")  # Hình dạng là rùa
        self.penup()  # Không vẽ đường khi di chuyển
        self.color("white")  # Màu sắc của rùa
        self.start_cross()  # Đặt vị trí bắt đầu cho rùa
        self.setheading(90)  # Đặt đầu rùa hướng lên trên

    def turtle_up(self):
        # Di chuyển rùa lên trên 10 đơn vị
        self.goto(self.xcor(), self.ycor() + 10)

    def turtle_down(self):
        # Di chuyển rùa xuống dưới 10 đơn vị
        self.goto(self.xcor(), self.ycor() - 10)

    def cross_success(self):
        # Kiểm tra nếu rùa vượt qua đường thành công (vượt qua mép trên màn hình)
        return self.ycor() > 260

    def start_cross(self):
        # Đặt rùa ở vị trí ban đầu (đáy màn hình)
        self.goto(0, -260)

# Quản lý các phương tiện giao thông
class VehicleManager:
    def __init__(self):
        self.vehicles = []  # Danh sách các phương tiện
        self.speed = 3  # Tốc độ di chuyển của xe
        self.min_distance = 30  # Khoảng cách tối thiểu giữa các xe

    def rand_vehicle(self, level):
        # Sinh ra phương tiện giao thông ngẫu nhiên dựa trên cấp độ
        num_vehicles = min(level, 7)  # Số xe sinh ra, giới hạn ở 7 xe
        for _ in range(num_vehicles):
            y_pos = random.randint(-220, 220)  # Vị trí ngẫu nhiên trên trục y
            # Kiểm tra nếu vị trí y của xe không trùng với các xe khác
            if not any(abs(y_pos - car.ycor()) < self.min_distance for car in self.vehicles):
                car = Turtle()
                car.shape("square")  # Hình dạng của xe là hình vuông
                car.shapesize(stretch_wid=1, stretch_len=2)  # Tạo hình chữ nhật cho xe
                car.penup()
                car.color(random.choice(COLORS))  # Chọn màu ngẫu nhiên cho xe
                car.goto(270, y_pos)  # Đặt xe vào vị trí bắt đầu
                self.vehicles.append(car)

    def move_vehicle(self):
        # Di chuyển tất cả các phương tiện sang trái
        for car in self.vehicles:
            car.backward(self.speed)
        # Loại bỏ các xe đã ra khỏi màn hình
        self.vehicles = [car for car in self.vehicles if car.xcor() > -320]

    def increment_speed(self):
        # Tăng tốc độ của các phương tiện
        self.speed += 3

# Quản lý điểm và cấp độ
class ScoreManager:
    def __init__(self):
        self.level = 1  # Cấp độ ban đầu
        self.display = Turtle()
        self.display.color("white")
        self.display.penup()
        self.display.hideturtle()  # Ẩn con trỏ turtle
        self.display.goto(-290, 270)
        self.update_display()

        self.high_score_display = Turtle()
        self.high_score_display.color("white")
        self.high_score_display.penup()
        self.high_score_display.hideturtle()
        self.high_score_display.goto(-100, 270)

    def update_display(self):
        # Cập nhật hiển thị cấp độ lên màn hình
        self.display.clear()  # Xóa hiển thị cũ
        self.display.write(f"Level: {self.level}", align="left", font=("Arial", 15, "normal"))

    def show_high_score(self, scores):
        # Hiển thị điểm cao nhất
        self.high_score_display.clear()
        if scores:
            self.high_score_display.write(f"High Score: {scores[0][1]} ({scores[0][0]})",
                                          align="center", font=("Arial", 15, "italic"))

    def increment_level(self):
        # Tăng cấp độ lên 1
        self.level += 1
        self.update_display()

    def game_over(self):
        # Hiển thị thông báo game over
        self.display.goto(0, 0)
        self.display.write("GAME OVER", align="center", font=("Arial", 30, "normal"))

# Tạo màn hình hiển thị
screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("Turtle Cross Game")
screen.tracer(0)

# Tạo các đối tượng
turtle_cross = TurtleCross()
vehicle_manager = VehicleManager()
score_manager = ScoreManager()
high_score_manager = HighScoreManager()

# Hiển thị điểm cao nhất
score_manager.show_high_score(high_score_manager.scores)

# Cài đặt điều khiển
screen.listen()
screen.onkey(turtle_cross.turtle_up, "Up")  # Di chuyển rùa lên khi nhấn phím Up
screen.onkey(turtle_cross.turtle_down, "Down")  # Di chuyển rùa xuống khi nhấn phím Down

# Vòng lặp chính của trò chơi
game_is_on = True
while game_is_on:
    time.sleep(0.06)  # Dừng trong 0.06 giây để điều chỉnh tốc độ trò chơi
    screen.update()  # Cập nhật màn hình
    vehicle_manager.rand_vehicle(score_manager.level)  # Sinh ra phương tiện
    vehicle_manager.move_vehicle()  # Di chuyển các phương tiện

    # Kiểm tra va chạm
    for car in vehicle_manager.vehicles:
        if car.distance(turtle_cross) < 20:  # Nếu rùa va vào xe
            game_is_on = False  # Kết thúc trò chơi
            score_manager.game_over()  # Hiển thị game over

            # Yêu cầu nhập tên người chơi và lưu điểm
            player_name = screen.textinput("Game Over", "Enter your name:")
            if player_name:
                high_score_manager.save_score(player_name, score_manager.level)

            # Hiển thị bảng điểm trong terminal
            high_score_manager.display_high_scores()
            screen.bye()  # Đóng màn hình

    # Kiểm tra nếu rùa qua đường thành công
    if turtle_cross.cross_success():
        turtle_cross.start_cross()  # Đặt lại vị trí rùa
        vehicle_manager.increment_speed()  # Tăng tốc độ xe
        score_manager.increment_level()  # Tăng cấp độ
