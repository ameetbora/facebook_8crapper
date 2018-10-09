"https://www.facebook.com/pages_reaction_units/more/?page_id=1657775594549456&cursor=%7B%22timeline_cursor%22%3A%222645646350%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D&surface=www_pages_community_tab&unit_count=8&__user=100029134355964&__a=1"

path = "https://www.facebook.com/pages_reaction_units/more/?"
page_id_param = "&page_id={pid}"
user_id_param = "&__user={uid}"
cursor = "&cursor=%7B%22timeline_cursor%22%3A%{cn}%22%2C%22timeline_section_cursor%22%3Anull%2C%22has_next_page%22%3Afalse%7D"
remaining_params = "&surface=www_pages_community_tab&unit_count=8&__a=1"

def page_url(page_id: int, user_id: int) -> str:
    return "".join([
            path,
            page_id_param.format(pid=page_id),
            cursor,
            user_id_param.format(uid=user_id),
            remaining_params,
    ])
