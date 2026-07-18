import socket
import time

TARGET_IP = "172.19.0.6"
PORT = 3610

REQUESTS = 100000  # ลดลงให้ควบคุมได้ (ปรับเพิ่มทีหลัง)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

instance = 1  # device เดียว fixed

start = time.time()

for req in range(REQUESTS):

    tid = req & 0xFFFF

    packet = bytes([
        0x10, 0x81,

        (tid >> 8) & 0xFF,
        tid & 0xFF,

        0x02, 0x91, instance,      # SEOJ (device เดียว)

        0x05, 0xFF, 0x01,          # Controller

        0x61,

        0x01,

        0x80,
        0x01,
        0x30
    ])

    sock.sendto(packet, (TARGET_IP, PORT))

    # optional debug ทุก 1000 packet
    if req % 1000 == 0:
        print(f"sent: {req}")

end = time.time()

sock.close()

print("Finished")
print("Time used:", end - start)
print("RPS:", REQUESTS / (end - start))


# import socket
# import time

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# for i in range(100000):
#     packet = b'\x05\xff\x01'
#     sock.sendto(packet, ("172.17.0.4", 3610))
#     time.sleep(0.0005)  # คุม rate


# test3


# import socket
# import time
# import csv

# TARGET_IP = "172.19.0.6"
# PORT = 3610

# # =========================
# # CONFIG EXPERIMENT
# # =========================

# PACKET_SIZES = [0, 50, 100, 200]      # bytes เพิ่ม payload
# REQUEST_RATES = [100000, 500000, 1000000]   # จำนวน packet ต่อรอบ

# RUNS_PER_TEST = 1  # เพิ่มเป็น 3-5 เพื่อ average ได้

# # =========================
# # UDP SOCKET
# # =========================
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# instance = 1

# results = []

# # =========================
# # EXPERIMENT LOOP
# # =========================
# for size in PACKET_SIZES:
#     for req_count in REQUEST_RATES:

#         for run in range(RUNS_PER_TEST):

#             print(f"\n[Test] size={size}, requests={req_count}, run={run}")

#             start = time.time()

#             for req in range(req_count):

#                 tid = req & 0xFFFF

#                 base_packet = bytes([
#                     0x10, 0x81,
#                     (tid >> 8) & 0xFF,
#                     tid & 0xFF,
#                     0x02, 0x91, instance,
#                     0x05, 0xFF, 0x01,
#                     0x61,
#                     0x01,
#                     0x80,
#                     0x01,
#                     0x30
#                 ])

#                 payload = bytes([0xAA] * size)
#                 packet = base_packet + payload

#                 sock.sendto(packet, (TARGET_IP, PORT))

#             end = time.time()

#             duration = end - start
#             rps = req_count / duration

#             print(f"Time: {duration:.4f}s | RPS: {rps:.2f}")

#             results.append([
#                 size,
#                 req_count,
#                 run,
#                 duration,
#                 rps
#             ])

# sock.close()

# # =========================
# # EXPORT CSV
# # =========================

# filename = "udp_load_test_results.csv"

# with open(filename, "w", newline="") as f:
#     writer = csv.writer(f)

#     writer.writerow([
#         "packet_size_bytes",
#         "request_count",
#         "run",
#         "duration_sec",
#         "requests_per_sec"
#     ])

#     writer.writerows(results)

# print("\nSaved to:", filename)