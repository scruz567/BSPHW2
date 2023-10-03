import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    @property
    def midpoint(self):
        return Point((self.start.x + self.end.x) / 2, (self.start.y + self.end.y) / 2)

# Node including Line Segment, Left Subtree, Right subtree
class BSPNode:
    def __init__(self, segment=None):
        self.segment = segment
        self.front = None
        self.back = None

def build_bsp_tree(segments, start_segment):
    if len(segments) == 0:
        return None

    # Choose the user-selected segment as the splitting line
    if start_segment in segments:
        split_segment = start_segment

    else: 
        split_segment = random.choice(segments)
    # Create the root node
    root = BSPNode(split_segment)

    front_segments = []
    back_segments = []

    for segment in segments:
        if segment == split_segment:
            continue
        if is_segment_in_front(segment, split_segment):
            front_segments.append(segment)
        elif is_segment_in_back(segment, split_segment):
            back_segments.append(segment)

    root.front = build_bsp_tree(front_segments, start_segment)
    root.back = build_bsp_tree(back_segments, start_segment)

    return root

def is_segment_in_front(segment, ref_segment):
    dir_ref = Point(ref_segment.end.x - ref_segment.start.x, ref_segment.end.y - ref_segment.start.y)

    # Calculate vectors from the reference segment to the start and end points of the 'segment'
    vec1 = Point(segment.start.x - ref_segment.start.x, segment.start.y - ref_segment.start.y)
    vec2 = Point(segment.end.x - ref_segment.start.x, segment.end.y - ref_segment.start.y)

    # Calculate cross products
    cross_product1 = vec1.x * dir_ref.y - vec1.y * dir_ref.x
    cross_product2 = vec2.x * dir_ref.y - vec2.y * dir_ref.x

    # Check if both cross products have the same sign
    if cross_product1 * cross_product2 > 0:
        return True  # 'segment' is in front of ref_segment
    else:
        return False

def is_segment_in_back(segment, ref_segment):
    # Calculate the direction vector of the reference segment
    reference_dir = Point(ref_segment.end.x - ref_segment.start.x, ref_segment.end.y - ref_segment.start.y)

    # Calculate a vector from the start point of the reference segment to the midpoint of 'segment'
    vec = Point(segment.midpoint.x - ref_segment.start.x, segment.midpoint.y - ref_segment.start.y)

    # Calculate the dot product
    dot_product = vec.x * reference_dir.x + vec.y * reference_dir.y

    # Check the sign of the dot product
    if dot_product < 0:
        return True  # 'segment' is behind 'reference_segment' within the BSP tree
    else:
        return False  # 'segment' is in front of or collinear with 'reference_segment' within the BSP tree

def in_order_traversal(root):
    if root:
        # Traverse the left subtree
        in_order_traversal(root.front)
        # Print the current node's value
        print(f"{root.segment.start.x},{root.segment.start.y} - {root.segment.end.x},{root.segment.end.y}")

        # Traverse the right subtree
        in_order_traversal(root.back)
        
if __name__ == "__main__":
    # some line segments
    segments = [
        LineSegment(Point(0, 8), Point(10, 8)),
        LineSegment(Point(0, 0), Point(0, 8)),
        LineSegment(Point(10, 0), Point(10, 8)),
        LineSegment(Point(0, 0), Point(10, 0)),
        LineSegment(Point(4, 3), Point(4, 5)),
        LineSegment(Point(5,3), Point(4,3)),
        LineSegment(Point(4, 5), Point(5,3))
        
    ]

    print("Line segments:")
    for j, segment in enumerate(segments):
        print(f"{j + 1}: {segment.start.x},{segment.start.y} - {segment.end.x},{segment.end.y}")

    while True:
        choice = input("Select the starting line (1-7): ")
        try:
            choice = int(choice)
            if 1 <= choice <= 7:
                selected_segment = segments[choice - 1]
                break
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid input")

    bsp_tree = build_bsp_tree(segments, selected_segment)
    in_order_traversal(bsp_tree)

