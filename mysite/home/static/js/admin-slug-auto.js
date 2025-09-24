// Автоматическое создание slug из названия
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Admin slug auto-generation script loaded');
    
    // Функция для создания slug из текста
    function createSlug(text) {
        return text
            .toLowerCase()
            .replace(/[^\w\s-]/g, '') // Убираем специальные символы
            .replace(/[\s_-]+/g, '-') // Заменяем пробелы и подчеркивания на дефисы
            .replace(/^-+|-+$/g, ''); // Убираем дефисы в начале и конце
    }
    
    // Для ProjectCategory
    const categoryNameField = document.querySelector('input[name="name"]');
    const categorySlugField = document.querySelector('input[name="slug"]');
    
    if (categoryNameField && categorySlugField) {
        console.log('✅ Found ProjectCategory fields');
        
        categoryNameField.addEventListener('input', function() {
            if (!categorySlugField.value || categorySlugField.value === '') {
                const slug = createSlug(this.value);
                categorySlugField.value = slug;
                console.log(`✅ Auto-generated slug: "${this.value}" -> "${slug}"`);
            }
        });
    }
    
    // Для ProjectPage (Project Name из Card Head 2 -> slug)
    const projectNameField = document.querySelector('input[name*="project_name"]');
    const pageSlugField = document.querySelector('input[name="slug"]');
    
    if (projectNameField && pageSlugField) {
        console.log('✅ Found ProjectPage fields (Project Name -> slug)');
        
        projectNameField.addEventListener('input', function() {
            if (!pageSlugField.value || pageSlugField.value === '') {
                const slug = createSlug(this.value);
                pageSlugField.value = slug;
                console.log(`✅ Auto-generated slug for ProjectPage: "${this.value}" -> "${slug}"`);
            }
        });
        
        // Также обрабатываем случай, когда Project Name уже заполнен
        if (projectNameField.value && (!pageSlugField.value || pageSlugField.value === '')) {
            const slug = createSlug(projectNameField.value);
            pageSlugField.value = slug;
            console.log(`✅ Auto-generated slug for existing ProjectPage: "${projectNameField.value}" -> "${slug}"`);
        }
    }
    
    // Для InfoPage
    const infoTitleField = document.querySelector('input[name="title"]');
    const infoSlugField = document.querySelector('input[name="slug"]');
    
    if (infoTitleField && infoSlugField && !pageTitleField) {
        console.log('✅ Found InfoPage fields');
        
        infoTitleField.addEventListener('input', function() {
            if (!infoSlugField.value || infoSlugField.value === '') {
                const slug = createSlug(this.value);
                infoSlugField.value = slug;
                console.log(`✅ Auto-generated slug: "${this.value}" -> "${slug}"`);
            }
        });
    }
});
