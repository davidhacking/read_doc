# [mooc](https://www.imooc.com/video/6243)

Input.GetAxis()"Horizontal" "Vertical"
GameObject.get 
Component.get
cammer.lookat

//左上 右下移动
Verctor3 direction = Input.GetAxis("Horizontal") * transform.right + Input.GetAxis("Vertical") * transform.forward
transform.position = transform.position + speed * Time.delaTime * direction

// 鼠标点击移动人物
void ClickOn(Vector2 pos) {
    if (player == null) {
        return;
    }
    Ray r = this.camera.SrceenPointToRay(pos);
    RaycastHit[] hits = Physics.RaycastAll(r);
    foreach (RaycastHit h in hits) {
        BoxCollider bc = h.collider as BoxCollider;
        if (bc != null && bc.name.Contains("floor")) {
            player.GetComponent<Player>().WalkTo(hit.point);
        }
    }
}