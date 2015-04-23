WITH access_data AS (
                WITH model_data AS (
                    WITH unique_model_data AS (
                        SELECT DISTINCT
                            ON (res_id) "module",
                            "name",
                            "res_id"
                        FROM
                            ir_model_data
                        WHERE
                            model = 'ir.model'
                        ORDER BY
                            res_id ASC,
                            "id" ASC
                    ) SELECT
                        ir_module_module."id" AS module_id,
                        ir_module_module."name" AS module_name,
                        ir_model."id" AS model_id,
                        ir_model."model" AS model_name,
                        unique_model_data."name" AS model_xml_id,
                        CONCAT (
                            ir_module_module."name",
                            '.',
                            unique_model_data."name"
                        ) AS model_fully_qualified_xml_id
                    FROM
                        ir_model
                    INNER JOIN unique_model_data
                        ON unique_model_data.res_id = ir_model."id"
                    INNER JOIN ir_module_module
                        ON ir_module_module."name" = unique_model_data."module"
                    ORDER BY
                        model_fully_qualified_xml_id
                ) SELECT
                    COALESCE(ir_model_access.perm_create, 'f') AS perm_create,
                    COALESCE(ir_model_access.perm_read, 'f') AS perm_read,
                    COALESCE(ir_model_access.perm_write, 'f') AS perm_write,
                    COALESCE(ir_model_access.perm_unlink, 'f') AS perm_unlink,
                    CASE WHEN perm_create = 't' THEN 8 ELSE 0 END +
                    CASE WHEN perm_read = 't' THEN 4 ELSE 0 END +
                    CASE WHEN perm_write = 't' THEN 2 ELSE 0 END +
                    CASE WHEN perm_unlink = 't' THEN 1 ELSE 0 END
                    AS crud,
                    model_data.*,
                    groups_implied.*
                FROM
                    model_data
                LEFT JOIN ir_model_access
                    ON model_data.model_id = ir_model_access.model_id
                LEFT JOIN report_groups_implied AS groups_implied
                    ON ir_model_access.group_id = groups_implied.implied_id
            ) SELECT
                ROW_NUMBER() OVER() AS "id",
                min(module_id) AS model_module_id,
                min(module_name) AS model_module_xml_id,
                model_id,
                min(model_name) AS model_name,
                min(model_xml_id) AS model_xml_id,
                min(model_fully_qualified_xml_id)
                    AS model_fully_qualified_xml_id,
                bool_or(perm_create) AS perm_create,
                bool_or(perm_read) AS perm_read,
                bool_or(perm_write) AS perm_write,
                bool_or(perm_unlink) AS perm_unlink,
                bit_or(crud) AS crud,
                min(group_category_id) AS group_category_id,
                min(group_category_fully_qualified_xml_id)
                    AS group_category_fully_qualified_xml_id,
                min(group_module_id) AS group_module_id,
                min(group_module_xml_id) AS group_module_xml_id,
                group_id,
                min(group_name) AS group_name,
                min(group_xml_id) AS group_xml_id,
                min(group_fully_qualified_xml_id)
                    AS group_fully_qualified_xml_id,
                min(implied_category_id) AS implied_category_id,
                min(implied_category_fully_qualified_xml_id)
                    AS implied_category_fully_qualified_xml_id,
                min(implied_module_id) AS implied_module_id,
                min(implied_module_xml_id) AS implied_module_xml_id,
                min(implied_id),
                min(implied_name) AS implied_name,
                min(implied_xml_id) AS implied_xml_id,
                min(implied_fully_qualified_xml_id)
                    AS implied_fully_qualified_xml_id
            FROM
                access_data
                        where model_id = 140
                        GROUP BY model_id, group_id
