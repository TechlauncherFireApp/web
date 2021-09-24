from domain import TenancyConfig


def get_all_configs(session):
    return session.query(TenancyConfig.id,
                         TenancyConfig.name,
                         TenancyConfig.title,
                         TenancyConfig.font,
                         TenancyConfig.navbar_colour,
                         TenancyConfig.background_colour,
                         TenancyConfig.deleted)


def get_active_config(session):
    return session.query(TenancyConfig.id,
                         TenancyConfig.name,
                         TenancyConfig.title,
                         TenancyConfig.font,
                         TenancyConfig.navbar_colour,
                         TenancyConfig.background_colour) \
        .filter(TenancyConfig.deleted == False) \
        .first()


def insert_config(session, config_name, config_title, config_font, config_navbar_colour, config_background_colour):
    session.query(TenancyConfig) \
        .filter(TenancyConfig.deleted == False) \
        .update({TenancyConfig.deleted: True})
    session.flush()
    config = TenancyConfig(name=config_name,
                           title=config_title,
                           font=config_font,
                           navbar_colour=config_navbar_colour,
                           background_colour=config_background_colour,
                           deleted=False)
    session.add(config)
    session.flush()
    return config.id


def toggle_config(session, config_id):
    session.query(TenancyConfig) \
        .filter(TenancyConfig.deleted == False) \
        .update({TenancyConfig.deleted: True})
    session.flush()
    existing_config = session.query(TenancyConfig) \
        .filter(TenancyConfig.id == config_id) \
        .first()
    if existing_config is None:
        return
    existing_config.deleted = False


def delete_config(session, config_id):
    existing_config = session.query(TenancyConfig) \
        .filter(TenancyConfig.id == config_id) \
        .first()
    if existing_config is None:
        return
    session.delete(existing_config)
