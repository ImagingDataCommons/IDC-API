from protorpc import messages


class MetadataRangesItem(messages.Message):
    
    age_at_initial_pathologic_diagnosis                               = messages.IntegerField(1, repeated=True, variant=messages.Variant.INT32)
    age_at_initial_pathologic_diagnosis_lte                           = messages.IntegerField(2, variant=messages.Variant.INT32)
    age_at_initial_pathologic_diagnosis_gte                           = messages.IntegerField(3, variant=messages.Variant.INT32)
    
    
    age_began_smoking_in_years                                        = messages.IntegerField(4, repeated=True, variant=messages.Variant.INT32)
    age_began_smoking_in_years_lte                                    = messages.IntegerField(5, variant=messages.Variant.INT32)
    age_began_smoking_in_years_gte                                    = messages.IntegerField(6, variant=messages.Variant.INT32)
    
    anatomic_neoplasm_subdivision                                     = messages.StringField(7, repeated=True)
    
    batch_number                                                      = messages.IntegerField(8, repeated=True, variant=messages.Variant.INT32)
    batch_number_lte                                                  = messages.IntegerField(9, variant=messages.Variant.INT32)
    batch_number_gte                                                  = messages.IntegerField(10, variant=messages.Variant.INT32)
    
    bcr                                                               = messages.StringField(11, repeated=True)
    
    bmi                                                               = messages.FloatField(12, repeated=True)
    bmi_lte                                                           = messages.FloatField(13)
    bmi_gte                                                           = messages.FloatField(14)
    
    case_barcode                                                      = messages.StringField(15, repeated=True)
    case_gdc_id                                                       = messages.StringField(16, repeated=True)
    clinical_M                                                        = messages.StringField(17, repeated=True)
    clinical_N                                                        = messages.StringField(18, repeated=True)
    clinical_stage                                                    = messages.StringField(19, repeated=True)
    clinical_T                                                        = messages.StringField(20, repeated=True)
    colorectal_cancer                                                 = messages.StringField(21, repeated=True)
    country                                                           = messages.StringField(22, repeated=True)
    
    days_to_birth                                                     = messages.IntegerField(23, repeated=True, variant=messages.Variant.INT32)
    days_to_birth_lte                                                 = messages.IntegerField(24, variant=messages.Variant.INT32)
    days_to_birth_gte                                                 = messages.IntegerField(25, variant=messages.Variant.INT32)
    
    
    days_to_death                                                     = messages.IntegerField(26, repeated=True, variant=messages.Variant.INT32)
    days_to_death_lte                                                 = messages.IntegerField(27, variant=messages.Variant.INT32)
    days_to_death_gte                                                 = messages.IntegerField(28, variant=messages.Variant.INT32)
    
    
    days_to_initial_pathologic_diagnosis                              = messages.IntegerField(29, repeated=True, variant=messages.Variant.INT32)
    days_to_initial_pathologic_diagnosis_lte                          = messages.IntegerField(30, variant=messages.Variant.INT32)
    days_to_initial_pathologic_diagnosis_gte                          = messages.IntegerField(31, variant=messages.Variant.INT32)
    
    
    days_to_last_followup                                             = messages.IntegerField(32, repeated=True, variant=messages.Variant.INT32)
    days_to_last_followup_lte                                         = messages.IntegerField(33, variant=messages.Variant.INT32)
    days_to_last_followup_gte                                         = messages.IntegerField(34, variant=messages.Variant.INT32)
    
    
    days_to_last_known_alive                                          = messages.IntegerField(35, repeated=True, variant=messages.Variant.INT32)
    days_to_last_known_alive_lte                                      = messages.IntegerField(36, variant=messages.Variant.INT32)
    days_to_last_known_alive_gte                                      = messages.IntegerField(37, variant=messages.Variant.INT32)
    
    
    days_to_submitted_specimen_dx                                     = messages.IntegerField(38, repeated=True, variant=messages.Variant.INT32)
    days_to_submitted_specimen_dx_lte                                 = messages.IntegerField(39, variant=messages.Variant.INT32)
    days_to_submitted_specimen_dx_gte                                 = messages.IntegerField(40, variant=messages.Variant.INT32)
    
    endpoint_type                                                     = messages.StringField(41, repeated=True)
    ethnicity                                                         = messages.StringField(42, repeated=True)
    gender                                                            = messages.StringField(43, repeated=True)
    
    gleason_score_combined                                            = messages.IntegerField(44, repeated=True, variant=messages.Variant.INT32)
    gleason_score_combined_lte                                        = messages.IntegerField(45, variant=messages.Variant.INT32)
    gleason_score_combined_gte                                        = messages.IntegerField(46, variant=messages.Variant.INT32)
    
    
    height                                                            = messages.IntegerField(47, repeated=True, variant=messages.Variant.INT32)
    height_lte                                                        = messages.IntegerField(48, variant=messages.Variant.INT32)
    height_gte                                                        = messages.IntegerField(49, variant=messages.Variant.INT32)
    
    histological_type                                                 = messages.StringField(50, repeated=True)
    history_of_colon_polyps                                           = messages.StringField(51, repeated=True)
    history_of_neoadjuvant_treatment                                  = messages.StringField(52, repeated=True)
    hpv_calls                                                         = messages.StringField(53, repeated=True)
    hpv_status                                                        = messages.StringField(54, repeated=True)
    h_pylori_infection                                                = messages.StringField(55, repeated=True)
    icd_10                                                            = messages.StringField(56, repeated=True)
    icd_o_3_histology                                                 = messages.StringField(57, repeated=True)
    icd_o_3_site                                                      = messages.StringField(58, repeated=True)
    lymphatic_invasion                                                = messages.StringField(59, repeated=True)
    lymphnodes_examined                                               = messages.StringField(60, repeated=True)
    lymphovascular_invasion_present                                   = messages.StringField(61, repeated=True)
    menopause_status                                                  = messages.StringField(62, repeated=True)
    mononucleotide_and_dinucleotide_marker_panel_analysis_status      = messages.StringField(63, repeated=True)
    neoplasm_histologic_grade                                         = messages.StringField(64, repeated=True)
    new_tumor_event_after_initial_treatment                           = messages.StringField(65, repeated=True)
    
    number_of_lymphnodes_examined                                     = messages.IntegerField(66, repeated=True, variant=messages.Variant.INT32)
    number_of_lymphnodes_examined_lte                                 = messages.IntegerField(67, variant=messages.Variant.INT32)
    number_of_lymphnodes_examined_gte                                 = messages.IntegerField(68, variant=messages.Variant.INT32)
    
    
    number_of_lymphnodes_positive_by_he                               = messages.IntegerField(69, repeated=True, variant=messages.Variant.INT32)
    number_of_lymphnodes_positive_by_he_lte                           = messages.IntegerField(70, variant=messages.Variant.INT32)
    number_of_lymphnodes_positive_by_he_gte                           = messages.IntegerField(71, variant=messages.Variant.INT32)
    
    
    number_pack_years_smoked                                          = messages.IntegerField(72, repeated=True, variant=messages.Variant.INT32)
    number_pack_years_smoked_lte                                      = messages.IntegerField(73, variant=messages.Variant.INT32)
    number_pack_years_smoked_gte                                      = messages.IntegerField(74, variant=messages.Variant.INT32)
    
    other_dx                                                          = messages.StringField(75, repeated=True)
    other_malignancy_anatomic_site                                    = messages.StringField(76, repeated=True)
    other_malignancy_histological_type                                = messages.StringField(77, repeated=True)
    other_malignancy_type                                             = messages.StringField(78, repeated=True)
    pathologic_M                                                      = messages.StringField(79, repeated=True)
    pathologic_N                                                      = messages.StringField(80, repeated=True)
    pathologic_stage                                                  = messages.StringField(81, repeated=True)
    pathologic_T                                                      = messages.StringField(82, repeated=True)
    person_neoplasm_cancer_status                                     = messages.StringField(83, repeated=True)
    pregnancies                                                       = messages.StringField(84, repeated=True)
    primary_neoplasm_melanoma_dx                                      = messages.StringField(85, repeated=True)
    primary_therapy_outcome_success                                   = messages.StringField(86, repeated=True)
    program_name                                                      = messages.StringField(87, repeated=True)
    project_disease_type                                              = messages.StringField(88, repeated=True)
    project_short_name                                                = messages.StringField(89, repeated=True)
    
    psa_value                                                         = messages.FloatField(90, repeated=True)
    psa_value_lte                                                     = messages.FloatField(91)
    psa_value_gte                                                     = messages.FloatField(92)
    
    race                                                              = messages.StringField(93, repeated=True)
    residual_tumor                                                    = messages.StringField(94, repeated=True)
    
    stopped_smoking_year                                              = messages.IntegerField(95, repeated=True, variant=messages.Variant.INT32)
    stopped_smoking_year_lte                                          = messages.IntegerField(96, variant=messages.Variant.INT32)
    stopped_smoking_year_gte                                          = messages.IntegerField(97, variant=messages.Variant.INT32)
    
    
    summary_file_count                                                = messages.IntegerField(98, repeated=True, variant=messages.Variant.INT32)
    summary_file_count_lte                                            = messages.IntegerField(99, variant=messages.Variant.INT32)
    summary_file_count_gte                                            = messages.IntegerField(100, variant=messages.Variant.INT32)
    
    tobacco_smoking_history                                           = messages.StringField(101, repeated=True)
    tss_code                                                          = messages.StringField(102, repeated=True)
    tumor_tissue_site                                                 = messages.StringField(103, repeated=True)
    tumor_type                                                        = messages.StringField(104, repeated=True)
    venous_invasion                                                   = messages.StringField(105, repeated=True)
    vital_status                                                      = messages.StringField(106, repeated=True)
    
    weight                                                            = messages.IntegerField(107, repeated=True, variant=messages.Variant.INT32)
    weight_lte                                                        = messages.IntegerField(108, variant=messages.Variant.INT32)
    weight_gte                                                        = messages.IntegerField(109, variant=messages.Variant.INT32)
    
    
    year_of_diagnosis                                                 = messages.IntegerField(110, repeated=True, variant=messages.Variant.INT32)
    year_of_diagnosis_lte                                             = messages.IntegerField(111, variant=messages.Variant.INT32)
    year_of_diagnosis_gte                                             = messages.IntegerField(112, variant=messages.Variant.INT32)
    
    
    year_of_tobacco_smoking_onset                                     = messages.IntegerField(113, repeated=True, variant=messages.Variant.INT32)
    year_of_tobacco_smoking_onset_lte                                 = messages.IntegerField(114, variant=messages.Variant.INT32)
    year_of_tobacco_smoking_onset_gte                                 = messages.IntegerField(115, variant=messages.Variant.INT32)
    
    
    avg_percent_lymphocyte_infiltration                               = messages.FloatField(116, repeated=True)
    avg_percent_lymphocyte_infiltration_lte                           = messages.FloatField(117)
    avg_percent_lymphocyte_infiltration_gte                           = messages.FloatField(118)
    
    
    avg_percent_monocyte_infiltration                                 = messages.FloatField(119, repeated=True)
    avg_percent_monocyte_infiltration_lte                             = messages.FloatField(120)
    avg_percent_monocyte_infiltration_gte                             = messages.FloatField(121)
    
    
    avg_percent_necrosis                                              = messages.FloatField(122, repeated=True)
    avg_percent_necrosis_lte                                          = messages.FloatField(123)
    avg_percent_necrosis_gte                                          = messages.FloatField(124)
    
    
    avg_percent_neutrophil_infiltration                               = messages.FloatField(125, repeated=True)
    avg_percent_neutrophil_infiltration_lte                           = messages.FloatField(126)
    avg_percent_neutrophil_infiltration_gte                           = messages.FloatField(127)
    
    
    avg_percent_normal_cells                                          = messages.FloatField(128, repeated=True)
    avg_percent_normal_cells_lte                                      = messages.FloatField(129)
    avg_percent_normal_cells_gte                                      = messages.FloatField(130)
    
    
    avg_percent_stromal_cells                                         = messages.FloatField(131, repeated=True)
    avg_percent_stromal_cells_lte                                     = messages.FloatField(132)
    avg_percent_stromal_cells_gte                                     = messages.FloatField(133)
    
    
    avg_percent_tumor_cells                                           = messages.FloatField(134, repeated=True)
    avg_percent_tumor_cells_lte                                       = messages.FloatField(135)
    avg_percent_tumor_cells_gte                                       = messages.FloatField(136)
    
    
    avg_percent_tumor_nuclei                                          = messages.FloatField(137, repeated=True)
    avg_percent_tumor_nuclei_lte                                      = messages.FloatField(138)
    avg_percent_tumor_nuclei_gte                                      = messages.FloatField(139)
    
    
    batch_number                                                      = messages.IntegerField(140, repeated=True, variant=messages.Variant.INT32)
    batch_number_lte                                                  = messages.IntegerField(141, variant=messages.Variant.INT32)
    batch_number_gte                                                  = messages.IntegerField(142, variant=messages.Variant.INT32)
    
    bcr                                                               = messages.StringField(143, repeated=True)
    case_barcode                                                      = messages.StringField(144, repeated=True)
    
    days_to_collection                                                = messages.IntegerField(145, repeated=True, variant=messages.Variant.INT32)
    days_to_collection_lte                                            = messages.IntegerField(146, variant=messages.Variant.INT32)
    days_to_collection_gte                                            = messages.IntegerField(147, variant=messages.Variant.INT32)
    
    
    days_to_sample_procurement                                        = messages.IntegerField(148, repeated=True, variant=messages.Variant.INT32)
    days_to_sample_procurement_lte                                    = messages.IntegerField(149, variant=messages.Variant.INT32)
    days_to_sample_procurement_gte                                    = messages.IntegerField(150, variant=messages.Variant.INT32)
    
    endpoint_type                                                     = messages.StringField(151, repeated=True)
    
    max_percent_lymphocyte_infiltration                               = messages.FloatField(152, repeated=True)
    max_percent_lymphocyte_infiltration_lte                           = messages.FloatField(153)
    max_percent_lymphocyte_infiltration_gte                           = messages.FloatField(154)
    
    
    max_percent_monocyte_infiltration                                 = messages.FloatField(155, repeated=True)
    max_percent_monocyte_infiltration_lte                             = messages.FloatField(156)
    max_percent_monocyte_infiltration_gte                             = messages.FloatField(157)
    
    
    max_percent_necrosis                                              = messages.FloatField(158, repeated=True)
    max_percent_necrosis_lte                                          = messages.FloatField(159)
    max_percent_necrosis_gte                                          = messages.FloatField(160)
    
    
    max_percent_neutrophil_infiltration                               = messages.FloatField(161, repeated=True)
    max_percent_neutrophil_infiltration_lte                           = messages.FloatField(162)
    max_percent_neutrophil_infiltration_gte                           = messages.FloatField(163)
    
    
    max_percent_normal_cells                                          = messages.FloatField(164, repeated=True)
    max_percent_normal_cells_lte                                      = messages.FloatField(165)
    max_percent_normal_cells_gte                                      = messages.FloatField(166)
    
    
    max_percent_stromal_cells                                         = messages.FloatField(167, repeated=True)
    max_percent_stromal_cells_lte                                     = messages.FloatField(168)
    max_percent_stromal_cells_gte                                     = messages.FloatField(169)
    
    
    max_percent_tumor_cells                                           = messages.FloatField(170, repeated=True)
    max_percent_tumor_cells_lte                                       = messages.FloatField(171)
    max_percent_tumor_cells_gte                                       = messages.FloatField(172)
    
    
    max_percent_tumor_nuclei                                          = messages.FloatField(173, repeated=True)
    max_percent_tumor_nuclei_lte                                      = messages.FloatField(174)
    max_percent_tumor_nuclei_gte                                      = messages.FloatField(175)
    
    
    min_percent_lymphocyte_infiltration                               = messages.FloatField(176, repeated=True)
    min_percent_lymphocyte_infiltration_lte                           = messages.FloatField(177)
    min_percent_lymphocyte_infiltration_gte                           = messages.FloatField(178)
    
    
    min_percent_monocyte_infiltration                                 = messages.FloatField(179, repeated=True)
    min_percent_monocyte_infiltration_lte                             = messages.FloatField(180)
    min_percent_monocyte_infiltration_gte                             = messages.FloatField(181)
    
    
    min_percent_necrosis                                              = messages.FloatField(182, repeated=True)
    min_percent_necrosis_lte                                          = messages.FloatField(183)
    min_percent_necrosis_gte                                          = messages.FloatField(184)
    
    
    min_percent_neutrophil_infiltration                               = messages.FloatField(185, repeated=True)
    min_percent_neutrophil_infiltration_lte                           = messages.FloatField(186)
    min_percent_neutrophil_infiltration_gte                           = messages.FloatField(187)
    
    
    min_percent_normal_cells                                          = messages.FloatField(188, repeated=True)
    min_percent_normal_cells_lte                                      = messages.FloatField(189)
    min_percent_normal_cells_gte                                      = messages.FloatField(190)
    
    
    min_percent_stromal_cells                                         = messages.FloatField(191, repeated=True)
    min_percent_stromal_cells_lte                                     = messages.FloatField(192)
    min_percent_stromal_cells_gte                                     = messages.FloatField(193)
    
    
    min_percent_tumor_cells                                           = messages.FloatField(194, repeated=True)
    min_percent_tumor_cells_lte                                       = messages.FloatField(195)
    min_percent_tumor_cells_gte                                       = messages.FloatField(196)
    
    
    min_percent_tumor_nuclei                                          = messages.FloatField(197, repeated=True)
    min_percent_tumor_nuclei_lte                                      = messages.FloatField(198)
    min_percent_tumor_nuclei_gte                                      = messages.FloatField(199)
    
    
    num_portions                                                      = messages.IntegerField(200, repeated=True, variant=messages.Variant.INT32)
    num_portions_lte                                                  = messages.IntegerField(201, variant=messages.Variant.INT32)
    num_portions_gte                                                  = messages.IntegerField(202, variant=messages.Variant.INT32)
    
    
    num_slides                                                        = messages.IntegerField(203, repeated=True, variant=messages.Variant.INT32)
    num_slides_lte                                                    = messages.IntegerField(204, variant=messages.Variant.INT32)
    num_slides_gte                                                    = messages.IntegerField(205, variant=messages.Variant.INT32)
    
    pathology_report_uuid                                             = messages.StringField(206, repeated=True)
    preservation_method                                               = messages.StringField(207, repeated=True)
    program_name                                                      = messages.StringField(208, repeated=True)
    project_disease_type                                              = messages.StringField(209, repeated=True)
    project_short_name                                                = messages.StringField(210, repeated=True)
    sample_barcode                                                    = messages.StringField(211, repeated=True)
    sample_gdc_id                                                     = messages.StringField(212, repeated=True)
    sample_type                                                       = messages.StringField(213, repeated=True)
    
class MetadataItem(messages.Message):
    age_at_initial_pathologic_diagnosis                               = messages.IntegerField(1, variant=messages.Variant.INT32)
    age_began_smoking_in_years                                        = messages.IntegerField(2, variant=messages.Variant.INT32)
    anatomic_neoplasm_subdivision                                     = messages.StringField(3)
    batch_number                                                      = messages.IntegerField(4, variant=messages.Variant.INT32)
    bcr                                                               = messages.StringField(5)
    bmi                                                               = messages.FloatField(6)
    case_barcode                                                      = messages.StringField(7)
    case_gdc_id                                                       = messages.StringField(8)
    clinical_M                                                        = messages.StringField(9)
    clinical_N                                                        = messages.StringField(10)
    clinical_stage                                                    = messages.StringField(11)
    clinical_T                                                        = messages.StringField(12)
    colorectal_cancer                                                 = messages.StringField(13)
    country                                                           = messages.StringField(14)
    days_to_birth                                                     = messages.IntegerField(15, variant=messages.Variant.INT32)
    days_to_death                                                     = messages.IntegerField(16, variant=messages.Variant.INT32)
    days_to_initial_pathologic_diagnosis                              = messages.IntegerField(17, variant=messages.Variant.INT32)
    days_to_last_followup                                             = messages.IntegerField(18, variant=messages.Variant.INT32)
    days_to_last_known_alive                                          = messages.IntegerField(19, variant=messages.Variant.INT32)
    days_to_submitted_specimen_dx                                     = messages.IntegerField(20, variant=messages.Variant.INT32)
    endpoint_type                                                     = messages.StringField(21)
    ethnicity                                                         = messages.StringField(22)
    gender                                                            = messages.StringField(23)
    gleason_score_combined                                            = messages.IntegerField(24, variant=messages.Variant.INT32)
    height                                                            = messages.IntegerField(25, variant=messages.Variant.INT32)
    histological_type                                                 = messages.StringField(26)
    history_of_colon_polyps                                           = messages.StringField(27)
    history_of_neoadjuvant_treatment                                  = messages.StringField(28)
    hpv_calls                                                         = messages.StringField(29)
    hpv_status                                                        = messages.StringField(30)
    h_pylori_infection                                                = messages.StringField(31)
    icd_10                                                            = messages.StringField(32)
    icd_o_3_histology                                                 = messages.StringField(33)
    icd_o_3_site                                                      = messages.StringField(34)
    lymphatic_invasion                                                = messages.StringField(35)
    lymphnodes_examined                                               = messages.StringField(36)
    lymphovascular_invasion_present                                   = messages.StringField(37)
    menopause_status                                                  = messages.StringField(38)
    mononucleotide_and_dinucleotide_marker_panel_analysis_status      = messages.StringField(39)
    neoplasm_histologic_grade                                         = messages.StringField(40)
    new_tumor_event_after_initial_treatment                           = messages.StringField(41)
    number_of_lymphnodes_examined                                     = messages.IntegerField(42, variant=messages.Variant.INT32)
    number_of_lymphnodes_positive_by_he                               = messages.IntegerField(43, variant=messages.Variant.INT32)
    number_pack_years_smoked                                          = messages.IntegerField(44, variant=messages.Variant.INT32)
    other_dx                                                          = messages.StringField(45)
    other_malignancy_anatomic_site                                    = messages.StringField(46)
    other_malignancy_histological_type                                = messages.StringField(47)
    other_malignancy_type                                             = messages.StringField(48)
    pathologic_M                                                      = messages.StringField(49)
    pathologic_N                                                      = messages.StringField(50)
    pathologic_stage                                                  = messages.StringField(51)
    pathologic_T                                                      = messages.StringField(52)
    person_neoplasm_cancer_status                                     = messages.StringField(53)
    pregnancies                                                       = messages.StringField(54)
    primary_neoplasm_melanoma_dx                                      = messages.StringField(55)
    primary_therapy_outcome_success                                   = messages.StringField(56)
    program_name                                                      = messages.StringField(57)
    project_disease_type                                              = messages.StringField(58)
    project_short_name                                                = messages.StringField(59)
    psa_value                                                         = messages.FloatField(60)
    race                                                              = messages.StringField(61)
    residual_tumor                                                    = messages.StringField(62)
    stopped_smoking_year                                              = messages.IntegerField(63, variant=messages.Variant.INT32)
    summary_file_count                                                = messages.IntegerField(64, variant=messages.Variant.INT32)
    tobacco_smoking_history                                           = messages.StringField(65)
    tss_code                                                          = messages.StringField(66)
    tumor_tissue_site                                                 = messages.StringField(67)
    tumor_type                                                        = messages.StringField(68)
    venous_invasion                                                   = messages.StringField(69)
    vital_status                                                      = messages.StringField(70)
    weight                                                            = messages.IntegerField(71, variant=messages.Variant.INT32)
    year_of_diagnosis                                                 = messages.IntegerField(72, variant=messages.Variant.INT32)
    year_of_tobacco_smoking_onset                                     = messages.IntegerField(73, variant=messages.Variant.INT32)
    avg_percent_lymphocyte_infiltration                               = messages.FloatField(74)
    avg_percent_monocyte_infiltration                                 = messages.FloatField(75)
    avg_percent_necrosis                                              = messages.FloatField(76)
    avg_percent_neutrophil_infiltration                               = messages.FloatField(77)
    avg_percent_normal_cells                                          = messages.FloatField(78)
    avg_percent_stromal_cells                                         = messages.FloatField(79)
    avg_percent_tumor_cells                                           = messages.FloatField(80)
    avg_percent_tumor_nuclei                                          = messages.FloatField(81)
    batch_number                                                      = messages.IntegerField(82, variant=messages.Variant.INT32)
    bcr                                                               = messages.StringField(83)
    case_barcode                                                      = messages.StringField(84)
    days_to_collection                                                = messages.IntegerField(85, variant=messages.Variant.INT32)
    days_to_sample_procurement                                        = messages.IntegerField(86, variant=messages.Variant.INT32)
    endpoint_type                                                     = messages.StringField(87)
    max_percent_lymphocyte_infiltration                               = messages.FloatField(88)
    max_percent_monocyte_infiltration                                 = messages.FloatField(89)
    max_percent_necrosis                                              = messages.FloatField(90)
    max_percent_neutrophil_infiltration                               = messages.FloatField(91)
    max_percent_normal_cells                                          = messages.FloatField(92)
    max_percent_stromal_cells                                         = messages.FloatField(93)
    max_percent_tumor_cells                                           = messages.FloatField(94)
    max_percent_tumor_nuclei                                          = messages.FloatField(95)
    min_percent_lymphocyte_infiltration                               = messages.FloatField(96)
    min_percent_monocyte_infiltration                                 = messages.FloatField(97)
    min_percent_necrosis                                              = messages.FloatField(98)
    min_percent_neutrophil_infiltration                               = messages.FloatField(99)
    min_percent_normal_cells                                          = messages.FloatField(100)
    min_percent_stromal_cells                                         = messages.FloatField(101)
    min_percent_tumor_cells                                           = messages.FloatField(102)
    min_percent_tumor_nuclei                                          = messages.FloatField(103)
    num_portions                                                      = messages.IntegerField(104, variant=messages.Variant.INT32)
    num_slides                                                        = messages.IntegerField(105, variant=messages.Variant.INT32)
    pathology_report_uuid                                             = messages.StringField(106)
    preservation_method                                               = messages.StringField(107)
    program_name                                                      = messages.StringField(108)
    project_disease_type                                              = messages.StringField(109)
    project_short_name                                                = messages.StringField(110)
    sample_barcode                                                    = messages.StringField(111)
    sample_gdc_id                                                     = messages.StringField(112)
    sample_type                                                       = messages.StringField(113)
    



class MetadataAnnotationItem(messages.Message):
    aliquot_barcode                = messages.StringField(1)
    annotation_gdc_id              = messages.StringField(2)
    annotation_submitter_id        = messages.StringField(3)
    case_barcode                   = messages.StringField(4)
    case_gdc_id                    = messages.StringField(5)
    category                       = messages.StringField(6)
    classification                 = messages.StringField(7)
    endpoint_type                  = messages.StringField(8)
    entity_barcode                 = messages.StringField(9)
    entity_gdc_id                  = messages.StringField(10)
    entity_type                    = messages.StringField(11)
    notes                          = messages.StringField(12)
    program_name                   = messages.StringField(13)
    project_short_name             = messages.StringField(14)
    sample_barcode                 = messages.StringField(15)
    status                         = messages.StringField(16)
    