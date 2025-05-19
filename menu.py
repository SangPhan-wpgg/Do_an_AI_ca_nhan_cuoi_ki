import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os

DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(os.path.abspath(__file__))
MAU_NEN_XAM = "#F0F0F0" # Màu xám nhạt
MAU_CHU_DEN = "#333333" # Màu chữ tối để dễ đọc trên nền xám

class UngDungChinh(tk.Tk):
    def __init__(self):
        super().__init__()
        CHIEU_RONG_MAN_HINH = self.winfo_screenwidth()
        CHIEU_DAI_MAN_HINH = self.winfo_screenheight()
        CHIEU_RONG_CUA_SO = 500
        CHIEU_DAI_CUA_SO = 280 # Điều chỉnh lại chiều cao nếu cần
        toa_do_x_cua_so = (CHIEU_RONG_MAN_HINH // 2) - (CHIEU_RONG_CUA_SO // 2)
        toa_do_y_cua_so = (CHIEU_DAI_MAN_HINH // 2) - (CHIEU_DAI_CUA_SO // 2)
        self.title("Đồ án AI cá nhân") 
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_DAI_CUA_SO}+{toa_do_x_cua_so}+{toa_do_y_cua_so}")
        self.configure(bg=MAU_NEN_XAM) # Đặt màu nền cho cửa sổ chính

        self.style = ttk.Style(self)
        self.style.theme_use('clam') # Hoặc 'alt', 'default', 'vista' tùy hệ điều hành và sở thích

        self.style.configure("TFrame", background=MAU_NEN_XAM)
        self.style.configure("TLabel", background=MAU_NEN_XAM, foreground=MAU_CHU_DEN, font=("Times New Roman", 15, "bold"))
        self.style.configure("TCombobox", font=("Times New Roman", 13))
        self.style.configure("TButton", font=("Times New Roman", 13), padding=5)
        # Cấu hình cho Listbox của Combobox (nếu cần, hơi phức tạp hơn)
        self.option_add('*TCombobox*Listbox.background', MAU_NEN_XAM)
        self.option_add('*TCombobox*Listbox.foreground', MAU_CHU_DEN)
        self.option_add('*TCombobox*Listbox.selectBackground', '#0078D7') # Màu khi chọn một mục
        self.option_add('*TCombobox*Listbox.selectForeground', 'white')


        self.khung_hien_tai = None
        self.hien_thi_khung(KhungLuaChonChinh)

    def hien_thi_khung(self, ten_khung_class):
        if self.khung_hien_tai:
            self.khung_hien_tai.destroy()
        self.khung_hien_tai = ten_khung_class(self, style="TFrame") 
        self.khung_hien_tai.pack(fill="both", expand=True, padx=10, pady=10)


class KhungLuaChonChinh(ttk.Frame):
    def __init__(self, khung_cha, **kwargs):
        super().__init__(khung_cha, **kwargs)
        self.khung_cha = khung_cha 
        
        label_chon_chuc_nang = ttk.Label(self, text="Chọn Chức Năng:")
        label_chon_chuc_nang.pack(pady=(10,5)) 
        self.cac_lua_chon_chuc_nang = [
            "Các bài toán chung",
            "Môi trường phức tạp",
            "Môi trường có ràng buộc",
            "Tìm Kiếm Trong MT Phức Tạp (AND/OR, Không/Một Phần QS)"
        ]
        
        self.bien_lua_chon_hien_tai = tk.StringVar()
        self.combobox_chuc_nang = ttk.Combobox(self, textvariable=self.bien_lua_chon_hien_tai, values=self.cac_lua_chon_chuc_nang, state="readonly", width=45)
        if self.cac_lua_chon_chuc_nang:
            self.combobox_chuc_nang.current(0)
        self.combobox_chuc_nang.pack(pady=5, padx=20, fill='x')

        self.nut_xac_nhan = ttk.Button(self, text="Thực Hiện", command=self.xu_ly_lua_chon_da_chon, width=20)
        self.nut_xac_nhan.pack(pady=(10,15))

    def xu_ly_lua_chon_da_chon(self):
        lua_chon = self.bien_lua_chon_hien_tai.get()
        if lua_chon == "Các bài toán chung":
            hien_thi_man_hinh_moi_truong_quan_sat_day_du()
        elif lua_chon == "Môi trường phức tạp":
            hien_thi_man_hinh_van_de_khong_cam_bien() 
        elif lua_chon == "Môi trường có ràng buộc":
            hien_thi_man_hinh_van_de_thoa_man_rang_buoc()
        elif lua_chon == "Tìm Kiếm Trong MT Phức Tạp (AND/OR, Không/Một Phần QS)":
            self.khung_cha.hien_thi_khung(KhungMoiTruongPhucTap)

class KhungMoiTruongPhucTap(ttk.Frame): # Sử dụng ttk.Frame
    def __init__(self, khung_cha, **kwargs):
        super().__init__(khung_cha, **kwargs)
        self.khung_cha = khung_cha
        
        label_chon_thuat_toan_mtp = ttk.Label(self, text="Chọn Thuật Toán (MT Phức Tạp):")
        label_chon_thuat_toan_mtp.pack(pady=(10,5))

        self.cac_lua_chon_mt_phuc_tap = [
            "Tìm Kiếm Đồ Thị AND/OR",
            "TK Không/Một Phần Quan Sát (Chung)"
        ]
        self.bien_lua_chon_mt_phuc_tap_hien_tai = tk.StringVar()
        self.combobox_mt_phuc_tap = ttk.Combobox(self, textvariable=self.bien_lua_chon_mt_phuc_tap_hien_tai, values=self.cac_lua_chon_mt_phuc_tap, state="readonly", width=40)
        if self.cac_lua_chon_mt_phuc_tap:
            self.combobox_mt_phuc_tap.current(0)
        self.combobox_mt_phuc_tap.pack(pady=5, padx=20, fill='x')

        self.nut_xac_nhan_mt_phuc_tap = ttk.Button(self, text="Thực Hiện", command=self.xu_ly_lua_chon_mt_phuc_tap_da_chon, width=20)
        self.nut_xac_nhan_mt_phuc_tap.pack(pady=10)
        
        self.nut_quay_lai = ttk.Button(self, text="Quay lại Menu Chính", command=lambda: self.khung_cha.hien_thi_khung(KhungLuaChonChinh), width=25)
        self.nut_quay_lai.pack(pady=(5,15))

    def xu_ly_lua_chon_mt_phuc_tap_da_chon(self):
        lua_chon = self.bien_lua_chon_mt_phuc_tap_hien_tai.get()
        if lua_chon == "Tìm Kiếm Đồ Thị AND/OR":
            hien_thi_man_hinh_tim_kiem_do_thi_and_or()
        elif lua_chon == "TK Không/Một Phần Quan Sát (Chung)":
            hien_thi_man_hinh_van_de_khong_cam_bien_phuc_tap()

def chay_file_con(ten_file):
    duong_dan_day_du = os.path.join(DUONG_DAN_THU_MUC_HIEN_HANH, ten_file)
    try:
        subprocess.run(["python", duong_dan_day_du], check=True)
    except FileNotFoundError:
        messagebox.showerror("Lỗi File", f"Không tìm thấy file:\n{ten_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Lỗi Thực Thi", f"Có lỗi khi chạy file:\n{ten_file}\n\n{e}")
    except Exception as e_all:
        messagebox.showerror("Lỗi Không Xác Định", f"Lỗi không xác định với file:\n{ten_file}\n\n{e_all}")

def hien_thi_man_hinh_moi_truong_quan_sat_day_du():
    chay_file_con("reinforcement_learning_main.py")

def hien_thi_man_hinh_tim_kiem_do_thi_and_or():
    chay_file_con("and_or_search_main.py")

def hien_thi_man_hinh_van_de_khong_cam_bien(): 
    chay_file_con("complex_environment_main.py") 

def hien_thi_man_hinh_van_de_khong_cam_bien_phuc_tap():
    chay_file_con("complex_environment_main.py")

def hien_thi_man_hinh_van_de_thoa_man_rang_buoc():
    chay_file_con("constrain_main.py")

ung_dung = UngDungChinh()
ung_dung.mainloop()