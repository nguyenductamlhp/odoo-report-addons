openerp.ir_export_extended_ept = function(instance) {
	var QWeb = instance.web.qweb,
		_t = instance.web._t;
	
	instance.web.DataExport.include({	
		
		
		events: {
			'click #add_field': function () {
	            var self = this;
	            this.$('#field-tree-structure tr.ui-selected')
	                .removeClass('ui-selected')
	                .find('a').each(function () {
	                    var id = $(this).attr('id').split('-')[1];
	                    var string = $(this).attr('string');
	                    self.add_field(id, string);
	                });
	        },
	        'click #remove_field': function () {
	            this.$('#fields_list option:selected').remove();
	        },
			'click #remove_all_field': function () {
				if (confirm(_t('Remove all fields?'))) {
					this.$('#fields_list').empty();
				} else {
					return false
				}
			},
			
			 'click #export_new_list': 'on_show_save_list',
		},
		
		start: function(){
	            var self = this;

	            //make all data type as default export
	            this.$el.find('#import_compat').val('');
	            
	            this._super();
	            
	            //adding up/down buttons
	            $(QWeb.render('ir_export_extended_ept.up_down')).insertAfter(this.$el.find('.oe_export_fields_selector_right'));
	            
	            //add up/down buttons events
	            this.$el.find('#field_up').click(function(){
	                up_el = self.$('#fields_list option:selected').first().prev();
	                if(up_el.length === 1){
	                    move_el = self.$('#fields_list option:selected').detach();
	                    up_el.before(move_el);
	                }
	            });
	            this.$el.find('#field_down').click(function(){
	                down_el = self.$('#fields_list option:selected').last().next();
	                if(down_el.length === 1){
	                    move_el = self.$('#fields_list option:selected').detach();
	                    down_el.after(move_el);
	                }
	            });
	        },
        do_setup_export_formats: function(formats) {
            this._super(formats);
            //Excel as default exported format if exist
            this.$el.find('#export_format').val('xls');
        },
		
	    do_save_export_list: function(value) {
	        var self = this;
	        var fields = self.get_fields();
	        if (!fields.length) {
	            return;
	        }
	        var seq = 0;
	        this.exports.create({
	            name: value,
	            resource: this.dataset.model,
	            domain: this.domain,
	            export_fields: _(fields).map(function (field) {
	            	seq++;
	            	var v = field['f_t'] ;
	                return [0, 0, {sequence:seq,name: field['f_v'],heading:v}];
	            })
	        }).then(function (export_list_id) {
	            if (!export_list_id) {
	                return;
	            }
	            if (!self.$el.find("#saved_export_list").length || self.$el.find("#saved_export_list").is(":hidden")) {
	                self.show_exports_list();
	            }
	            self.$el.find("#saved_export_list").append( new Option(value, export_list_id) );
	        });
	        this.on_show_save_list();
	    },
	    
	    show_exports_list: function() {
	        var self = this;
	        if (self.$el.find('#saved_export_list').is(':hidden')) {
	            self.$el.find('#ExistsExportList').show();
	            return $.when();
	        }
	        return this.exports.read_slice(['name'], {
	            domain: [['resource', '=', this.dataset.model]]
	        }).done(function (export_list) {
	            if (!export_list.length) {
	                return;
	            }
	            self.$el.find('#ExistsExportList').append(QWeb.render('Exists.ExportList', {'existing_exports': export_list}));
	            self.$el.find('#saved_export_list').change(function() {
	                self.$el.find('#fields_list option').remove();
	                var export_id = self.$el.find('#saved_export_list option:selected').val();
	                if (export_id) {
	                    self.rpc('/web/export/namelist', {'model': self.dataset.model, export_id: parseInt(export_id, 10)}).done(self.do_load_export_field);
	                }
	            });
	            self.$el.find('#delete_export_list').click(function() {
	            	if (confirm(_t('Delete saved list?'))) {
		                var select_exp = self.$el.find('#saved_export_list option:selected');
		                if (select_exp.val()) {
		                    self.exports.unlink([parseInt(select_exp.val(), 10)]);
		                    select_exp.remove();
		                    self.$el.find("#fields_list option").remove();
		                    if (self.$el.find('#saved_export_list option').length <= 1) {
		                        self.$el.find('#ExistsExportList').hide();
		                    }
		                }
	            	}
	            });
	        });
	    },

	    get_fields: function() {
	        var export_fields = this.$("#fields_list option").map(function() {
	            var val_ept = {'f_v':$(this).val(),'f_t':$(this).text()}
	        	return val_ept;
	        }).get();
	        if (!export_fields.length) {
	            alert(_t("Please select fields to save export list..."));
	        }
	        return export_fields;
	    },
	    
	});
};