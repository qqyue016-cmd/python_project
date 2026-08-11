# ————————学生成绩管理系统————————
# 学生类
class Student:
    def __init__(self,name:str,score:int):
        self.name=name
        self.score=score

    def __str__(self):
        return f'{self.name}的成绩为:{self.score}'

    def __lt__(self, other):
        return self.score<other.score

# 1. 添加学生（姓名 + 分数）
# 成绩管理系统类
class ScoreManagementSystem:
    def __init__(self):
        self.students_list=[]

    def add_student(self):
        name = input('请输入学生姓名:')
        for s in self.students_list:
            if s.name == name :
                print('该学生已存在')
                return
        score = int(input('请输入学生成绩:'))
        student = Student(name,score)
        self.students_list.append(student)

# 2. 查看所有学生
    def show_all_students(self):
        if self.students_list == []:
            print('系统内未添加学生')
        else:
            for s in self.students_list:
                print(s)
# 3. 按分数排序
    def rank(self):
        if self.students_list == []:
            print('系统内未添加学生')
        else:
            self.students_list.sort(reverse=True)
            for s in self.students_list:
                print(s)
# 4. 计算平均分
    def average_score(self):
        if self.students_list == []:
            print('系统内未添加学生')
        else:
            total = 0
            for s in self.students_list:
                total+= s.score
            print(f'平均分为：{total/len(self.students_list)}')

# 5. 删除学生
    def delete_students(self):
        name = input('请输入学生姓名:')
        for s in self.students_list:
            if s.name == name:
                self.students_list.remove(s)
                print('已删除成功')
                return
        print('该学生不存在')
# 6. 修改成绩
    def change_students(self):
        name = input('请输入学生姓名')
        for s in self.students_list:
            if s.name == name :
                score = int(input('请输入新的成绩'))
                s.score = score
                print('修改成功')
                return
        print('该学生不存在')

# 主菜单
    def run(self):
        while True:
            print('\n========== 教务管理系统 ==========')
            print('1. 添加学生信息')
            print('2. 修改学生信息')
            print('3. 删除学生信息')
            print('4. 按成绩排序')
            print('5. 计算平均分')
            print('6. 显示所有学生信息')
            print('0. 退出系统')
            print('==================================')
            choice = input('请输入序号:')

            try:
                if choice == '1':
                    self.add_student()
                elif choice == '2':
                    self.change_students()
                elif choice == '3':
                    self.delete_students()
                elif choice == '4':
                    self.rank()
                elif choice == '5':
                    self.average_score()
                elif choice == '6':
                    self.show_all_students()
# 7. 退出
                elif choice == '0':
                    print('感谢使用')
                    break
                else:
                    print('输入号码无效，请重新输入')

# 异常处理
            except Exception as e:
                print(f'发现{e}错误')


if __name__ == '__main__':
    system = ScoreManagementSystem()
    system.run()

